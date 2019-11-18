from jsonrpcclient.clients.http_client import HTTPClient
from jsonrpcclient.requests import Request


class Rpc:
    def __init__(self, node: str, devel: bool):
        self.client = HTTPClient(node)

    def ping(self):
        payload = Request("ping")
        self.client.send(payload)

    def version(self):
        payload = Request("version")
        response = self.client.send(payload)

        return response.result

    def commit_hash(self):
        payload = Request("commitHash")
        response = self.client.send(payload)

        return response.result
