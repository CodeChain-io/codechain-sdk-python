from typing import Union

from jsonrpcclient.requests import Request


class Mempool:
    def __init__(self, client):
        self.client = client

    def send_signed_transaction(self, tx: str):
        payload = Request("mempool_sendSignedTransaction", tx)
        response = self.client.send(payload)

        return response.data.result

    def get_error_hint(self, transaction_hash: str):
        payload = Request("mempool_getErrorHint", transaction_hash)
        response = self.client.send(payload)

        return response.data.result

    def get_transaction_results_by_tracker(self, tracker: str):
        payload = Request("mempool_getTransactionResultsByTracker", tracker)
        response = self.client.send(payload)

        return response.data.result

    def get_pending_transactions(
        self, tx_from: Union[int, None], tx_to: Union[int, None]
    ):
        payload = Request("mempool_getPendingTransactions", tx_from, tx_to)
        response = self.client.send(payload)

        return response.data.result
