from typing import List

from ...rpc import Rpc as Rpc_thin
from .account import AccountRpc
from .chain import ChainRpc


class Rpc:
    def __init__(
        self,
        server: str,
        transaction_signer: str = None,
        fallback_servers: List[str] = None,
    ):
        self.server = server
        self.fallback_servers = fallback_servers
        self.chain = ChainRpc(self, transaction_signer)
        self.account = AccountRpc(self)

    def send_rpc_request(self, group: str, name: str, *args):
        all_servers = (
            [self.server]
            if self.fallback_servers is None
            else [self.server] + self.fallback_servers
        )
        errors = []

        for server in all_servers:
            try:
                rpc = Rpc_thin(server, devel=True)
                group = getattr(rpc, group, lambda: "Invalid rpc group")
                method = getattr(group, name, lambda: "Invalid rpc")
                return method(*args)
            except Exception as e:
                errors.append(e)

        raise ValueError(errors)
