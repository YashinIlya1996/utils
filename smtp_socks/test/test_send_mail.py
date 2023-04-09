import os
import unittest
from pathlib import Path
from smtp_socks.send_mail_proxy import send_mail


class TestSendMail(unittest.TestCase):
    def setUp(self):
        test_env_path = Path(__file__).parent / 'test.env'
        for row in test_env_path.read_text().splitlines():
            if row:
                name_, val_ = row.split('=')
                os.environ[name_] = val_

        self.addr_from = os.getenv('EMAIL_ADDR_FROM')
        self.addr_to = os.getenv('EMAIL_ADDR_TO')
        self.password = os.getenv('SMTP_PASSWORD')
        self.smtp_host = os.getenv('SMTP_HOST')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.body = 'Test email body'
        self.attachments = [Path(__file__).parent / 'test_attachment.txt',
                            Path(__file__).parent / 'test_attachment.png']

    def test_simple_send_mail_without_proxy(self):
        send_mail(self.addr_from, self.smtp_host, self.smtp_port, self.password,
                  self.addr_to, self.body, 'Test email subject')

    def test_send_mail_with_attachments_without_proxy(self):
        send_mail(self.addr_from, self.smtp_host, self.smtp_port, self.password,
                  self.addr_to, self.body, 'Test email attachments subject', attachments=self.attachments)

    def test_send_mail_with_proxy(self):
        send_mail(self.addr_from, self.smtp_host, self.smtp_port, self.password,
                  self.addr_to, self.body, 'Test email with proxy', attachments=self.attachments, via_proxy=True)


if __name__ == '__main__':
    unittest.main()
