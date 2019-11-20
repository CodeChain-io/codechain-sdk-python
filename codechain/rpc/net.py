from typing import Union

from jsonrpcclient.requests import Request


class Net:
    def __init__(self, client):
        self.client = client

    def locak_key_for(self, address: str, port: int):
        payload = Request("net_localKeyFor", address=address, port=port)
        response = self.client.send(payload)

        return response.result

    def register_remote_key_for(self, address: str, port: int, remote_public_key: str):
        payload = Request(
            "net_registerRemoteKeyFor",
            address=address,
            port=port,
            remotePublicKey=remote_public_key,
        )
        response = self.client.send(payload)

        return response.result

    def connect(self, address: str, port: int):
        payload = Request("net_connect", address=address, port=port)
        response = self.client.send(payload)

        return response.result

    def is_connected(self, address: str, port: int):
        payload = Request("net_isConnected", address=address, port=port)
        response = self.client.send(payload)

        return response.result

    def disconnect(self, address: str, port: int):
        payload = Request("net_disconnect", address=address, port=port)
        response = self.client.send(payload)

        return response.result

    def get_peer_count(self):
        payload = Request("net_getPeerCount")
        response = self.client.send(payload)

        return response.result

    def get_establiched_peers(self):
        payload = Request("net_getEstablishedPeers")
        response = self.client.send(payload)

        return response.result

    def get_port(self):
        payload = Request("net_getPort")
        response = self.client.send(payload)

        return response.result

    def add_to_whitelist(self, address: str, tag: Union[str, None]):
        payload = Request("net_addToWhitelist", address=address, tag=tag)
        response = self.client.send(payload)

        return response.result

    def remove_from_whitelist(self, address: str):
        payload = Request("net_removeFromWhitelist", address=address)
        response = self.client.send(payload)

        return response.result

    def add_to_blacklist(self, address: str, tag: Union[str, None]):
        payload = Request("net_addToBlacklist", address=address, tag=tag)
        response = self.client.send(payload)

        return response.result

    def remove_from_blacklist(self, address: str):
        payload = Request("net_removeFromBlacklist", address=address)
        response = self.client.send(payload)

        return response.result

    def enable_whitelist(self, address: str):
        payload = Request("net_enableWhitelist")
        response = self.client.send(payload)

        return response.result

    def disableWhitelist(self):
        payload = Request("net_disableWhitelist")
        response = self.client.send(payload)

        return response.result

    def enable_blacklist(self):
        payload = Request("net_enableBlacklist")
        response = self.client.send(payload)

        return response.result

    def disable_blacklist(self):
        payload = Request("net_disableBlacklist")
        response = self.client.send(payload)

        return response.result

    def get_whitelist(self, address: str):
        payload = Request("net_getWhitelist")
        response = self.client.send(payload)

        return response.result

    def get_blacklist(self, address: str):
        payload = Request("net_getBlacklist", address=address)
        response = self.client.send(payload)

        return response.result

    def recent_network_usage(self, address: str):
        payload = Request("net_recentNetworkUsage")
        response = self.client.send(payload)

        return response.result
