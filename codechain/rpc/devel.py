from typing import Union

from jsonrpcclient.requests import Request


class Devel:
    def __init__(self, client):
        self.client = client

    def get_state_trie_keys(self, offset: int, limit: int):
        payload = Request("devel_getStateTrieKeys", offset=offset, limit=limit)
        response = self.client.send(payload)

        return response.result

    def get_state_trie_value(self, key: str):
        payload = Request("devel_getStateTrieValue", key=key)
        response = self.client.send(payload)

        return response.result

    def start_sealing(self):
        payload = Request("devel_startSealing")
        response = self.client.send(payload)

        return response.result

    def stop_sealing(self):
        payload = Request("devel_stopSealing")
        response = self.client.send(payload)

        return response.result

    def get_block_sync_peers(self):
        payload = Request("devel_getBlockSyncPeers")
        response = self.client.send(payload)

        return response.result

    def test_tps(self, count: int, seed: int, option: str):
        if (
            option != "payOnly"
            and option != "transferSingle"
            and option != "transferMultiple"
            and option != "payOrTransfer"
        ):
            raise ValueError(
                f"option should be one of payOnly | transferSingle | transferMultiple | payOrTransfer"
            )

        payload = Request("devel_testTPS", count=count, seed=seed, option=option)
        response = self.client.send(payload)

        return response.result
