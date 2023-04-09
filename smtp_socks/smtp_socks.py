import smtplib
import os
from types import NoneType
from typing import Optional, Union, TypeAlias
from collections.abc import Iterable

import socks
from dataclasses import dataclass, asdict, fields

SockOpt: TypeAlias = Union[tuple[int, int, Union[int, bytes]], tuple[int, int, NoneType, int]]
DEFAULT_SOCKS_PORT = 1080


@dataclass
class ProxyConnectionConf:
    """ class to provide proxy-conf in SMTP._get_socket method """
    proxy_addr: str
    proxy_port: int = DEFAULT_SOCKS_PORT
    proxy_type: int = socks.PROXY_TYPE_SOCKS5
    proxy_rdns: bool = True
    proxy_username: Optional[str] = None
    proxy_password: Optional[str] = None
    socket_options: Optional[Iterable[SockOpt]] = None

    @classmethod
    def from_env(cls) -> "ProxyConnectionConf":
        env_map = {'proxy_addr': str, 'proxy_port': int, 'proxy_username': str, 'proxy_password': str}
        kwargs = {name_: type_(env_val) if (env_val := os.getenv(name_.upper())) else getattr(cls, name_)
                  for name_, type_ in env_map.items()}
        return cls(**kwargs)


class SOCKS_SMTP_SSL(smtplib.SMTP_SSL):
    def __init__(self, *args, proxy_conf: ProxyConnectionConf, **kwargs):
        self.proxy_conf = proxy_conf
        super().__init__(*args, **kwargs)

    def _get_socket(self, host, port, timeout):
        new_socket = socks.create_connection((host, port), timeout, self.source_address, **asdict(self.proxy_conf))
        new_socket = self.context.wrap_socket(new_socket, server_hostname=self._host)
        return new_socket
