from .aliases import PathLike
from typing import NamedTuple, Optional

class SSHAuth(NamedTuple):
    hostaddr: str
    hostport: int
    hostname: Optional[str]
    username: Optional[str]
    password: Optional[str]
    identity: Optional[str]
    identity_password: Optional[str]
    @property
    def socket(self): ...
    @property
    def destination(self): ...
    def enter_password(self, password: str) -> SSHAuth: ...
    def enter_identity_password(self, password: str) -> SSHAuth: ...
    @staticmethod
    def from_file(hostname: str, path: Optional[PathLike] = ...) -> SSHAuth: ...
    @staticmethod
    def cast(auth: LikeSSHAuth) -> SSHAuth: ...
