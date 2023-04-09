import logging
from collections.abc import Iterable
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from smtplib import SMTP_SSL
from typing import Optional

from .smtp_socks import ProxyConnectionConf, SOCKS_SMTP_SSL


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def send_mail(addr_from: str, smtp_host: str, smtp_port: int, smtp_password: str,
              addr_to: str, body: str, subject: Optional[str] = None,
              html_: bool = True, attachments: Optional[Iterable[Path]] = None,
              via_proxy: bool = False, proxy_conf: Optional[ProxyConnectionConf] = None):
    if via_proxy and proxy_conf is None:
        proxy_conf = ProxyConnectionConf.from_env()

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html' if html_ else 'plain'))

    for file_path in attachments or []:
        if not file_path.is_file():
            logger.warning(f'File {file_path} not found!')
            continue
        part = MIMEApplication(file_path.read_bytes(), Name=file_path.name)
        part['Content-Disposition'] = f'attachment; filename={file_path.name}'
        msg.attach(part)

    try:
        if via_proxy:
            server = SOCKS_SMTP_SSL(smtp_host, smtp_port, proxy_conf=proxy_conf)
        else:
            server = SMTP_SSL(smtp_host, smtp_port)
        server.login(addr_from, smtp_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        logger.exception(f'Error send mail from {addr_from} to {addr_to}!', exc_info=e)
        raise
    else:
        logger.info(f'Sent mail from {addr_from} to {addr_to}')

