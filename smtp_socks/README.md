# Description

Python `smtplib` module does not provide functionality to send emails via SOCKS-proxy.

`smtp_socks.py` contains:

- `SOCKS_SMTP_SSL` class that overrides receiving a socket for sending via proxy.
- `ProxyConnectionConf` dataclass to provide conf explicitly or from environment

`send_mail_proxy.py` contains:

- `send_mail` function that can use `SOCKS_SMTP_SSL` for sending mail via proxy, if it specified

# Usage

```python
from pathlib import Path
from smtp_socks import send_mail, ProxyConnectionConf

proxy_conf = ProxyConnectionConf(proxy_addr='proxy.mydomain.com')

send_mail(
    addr_from='example_from@mail.com',
    smtp_host='smtp.example.com',
    smtp_port=465,
    smtp_password='password',
    addr_to='example_to@mail.com',
    body='Hello!',
    subject='Subject of mail',
    html_=True,  # plain or html content-type of mail
    attachments=[Path('../files/chart.img'), Path('../files/report.xlsx')],
    via_proxy=True,  # if False will be used smtplib.SMTP_SSL server
    proxy_conf=proxy_conf,  # if None proxy configuration will be used environment vars
)
```