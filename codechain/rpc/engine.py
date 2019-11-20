from typing import Union

from jsonrpcclient.requests import Request


class Engine:
    def __init__(self, client):
        self.client = client

    def get_coinbase(self):
        payload = Request("engine_getCoinbase")
        response = self.client.send(payload)

        return response.result

    def get_block_reward(self, block_number: Union[int, None]):
        payload = Request("engine_getBlockReward", blockNumber=block_number)
        response = self.client.send(payload)

        return response.result

    def get_recommended_confirmation(self):
        payload = Request("engine_getRecommendedConfirmation")
        response = self.client.send(payload)

        return response.result

    def get_custom_action_data(
        self, handler_id: int, data_bytes: str, block_number: Union[int, None]
    ):
        payload = Request(
            "engine_getCustomActionData",
            handlerID=handler_id,
            bytes=data_bytes,
            blockNumber=block_number,
        )
        response = self.client.send(payload)

        return response.result
