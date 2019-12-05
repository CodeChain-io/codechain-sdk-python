from jsonrpcclient.clients.http_client import HTTPClient
from jsonrpcclient.requests import Request

from .Account import Account
from .Chain import Chain
from .Devel import Devel
from .Engine import Engine
from .Mempool import Mempool
from .Net import Net


class Rpc:
    def __init__(self, node: str, devel=False):
        self.client = HTTPClient(node)

        self.account = Account(self.client)
        self.chain = Chain(self.client)
        self.engine = Engine(self.client)
        self.mempool = Mempool(self.client)
        self.net = Net(self.client)
        if devel:
            self.devel = Devel(self.client)

    def ping(self):
        payload = Request("ping")
        self.client.send(payload)

    def version(self):
        payload = Request("version")
        response = self.client.send(payload)

        return response.data.result

    def commit_hash(self):
        payload = Request("commitHash")
        response = self.client.send(payload)

        return response.data.result
