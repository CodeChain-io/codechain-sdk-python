import binascii
from typing import Union

from jsonrpcclient.requests import Request


class Net:
    def __init__(self, client):
        self.client = client

    def locak_key_for(self, address: str, port: int):
        payload = Request("net_localKeyFor", address, port)
        response = self.client.send(payload)

        return response.data.result

    def register_remote_key_for(self, address: str, port: int, remote_public_key):
        if isinstance(remote_public_key, bytes):
            remote_public_key = "0x" + binascii.hexlify(remote_public_key).decode(
                "ascii"
            )
        payload = Request("net_registerRemoteKeyFor", address, port, remote_public_key,)
        response = self.client.send(payload)

        return response.data.result

    def connect(self, address: str, port: int):
        payload = Request("net_connect", address, port)
        response = self.client.send(payload)

        return response.data.result

    def is_connected(self, address: str, port: int):
        payload = Request("net_isConnected", address, port)
        response = self.client.send(payload)

        return response.data.result

    def disconnect(self, address: str, port: int):
        payload = Request("net_disconnect", address, port)
        response = self.client.send(payload)

        return response.data.result

    def get_peer_count(self):
        payload = Request("net_getPeerCount")
        response = self.client.send(payload)

        return response.data.result

    def get_establiched_peers(self):
        payload = Request("net_getEstablishedPeers")
        response = self.client.send(payload)

        return response.data.result

    def get_port(self):
        payload = Request("net_getPort")
        response = self.client.send(payload)

        return response.data.result

    def add_to_whitelist(self, address: str, tag: Union[str, None]):
        payload = Request("net_addToWhitelist", address, tag)
        response = self.client.send(payload)

        return response.data.result

    def remove_from_whitelist(self, address: str):
        payload = Request("net_removeFromWhitelist", address)
        response = self.client.send(payload)

        return response.data.result

    def add_to_blacklist(self, address: str, tag: Union[str, None]):
        payload = Request("net_addToBlacklist", address, tag)
        response = self.client.send(payload)

        return response.data.result

    def remove_from_blacklist(self, address: str):
        payload = Request("net_removeFromBlacklist", address)
        response = self.client.send(payload)

        return response.data.result

    def enable_whitelist(self, address: str):
        payload = Request("net_enableWhitelist")
        response = self.client.send(payload)

        return response.data.result

    def disableWhitelist(self):
        payload = Request("net_disableWhitelist")
        response = self.client.send(payload)

        return response.data.result

    def enable_blacklist(self):
        payload = Request("net_enableBlacklist")
        response = self.client.send(payload)

        return response.data.result

    def disable_blacklist(self):
        payload = Request("net_disableBlacklist")
        response = self.client.send(payload)

        return response.data.result

    def get_whitelist(self, address: str):
        payload = Request("net_getWhitelist")
        response = self.client.send(payload)

        return response.data.result

    def get_blacklist(self, address: str):
        payload = Request("net_getBlacklist", address)
        response = self.client.send(payload)

        return response.data.result

    def recent_network_usage(self):
        payload = Request("net_recentNetworkUsage")
        response = self.client.send(payload)

        return response.data.result
