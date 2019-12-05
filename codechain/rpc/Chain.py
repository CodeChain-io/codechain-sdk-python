from typing import List
from typing import Union

from jsonrpcclient.requests import Request


class Chain:
    def __init__(self, client):
        self.client = client

    def get_block_number(self):
        payload = Request("chain_getBestBlocknumber")
        response = self.client.send(payload)

        return response.data.result

    def get_best_block_id(self):
        payload = Request("chain_getBestBlockId")
        response = self.client.send(payload)

        return response.data.result

    def get_block_hash(self, block_number: Union[int, None]):
        payload = Request("chain_getBlockHash", block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_block_by_number(self, block_number: Union[int, None]):
        payload = Request("chain_getBlockByNumber", block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_block_by_hash(self, block_hash: str):
        payload = Request("chain_getBlockByHash", block_hash)
        response = self.client.send(payload)

        return response.data.result

    def get_block_transaction_count_by_hash(self, block_hash: str):
        payload = Request("chain_getBlockTransactionCountByHash", block_hash)
        response = self.client.send(payload)

        return response.data.result

    def get_transaction(self, transaction_hash: str):
        payload = Request("chain_getTransaction", transaction_hash)
        response = self.client.send(payload)

        return response.data.result

    def get_transaction_signer(self, transaction_hash: str):
        payload = Request("chain_getTransactionSigner", transaction_hash)
        response = self.client.send(payload)

        return response.data.result

    def contains_transaction(self, transaction_hash: str):
        payload = Request("chain_containsTransaction", transaction_hash)
        response = self.client.send(payload)

        return response.data.result

    def get_transaction_by_tracker(self, tracker: str):
        payload = Request("chain_getTransactionByTracker", tracker)
        response = self.client.send(payload)

        return response.data.result

    def get_asset_scheme_by_tracker(
        self, tracker: str, shard_id: int, block_number: Union[int, None]
    ):
        payload = Request(
            "chain_getAsset_schemeByTracker", tracker, shard_id, block_number,
        )
        response = self.client.send(payload)

        return response.data.result

    def get_asset_scheme_by_type(
        self, asset_type: str, shard_id: int, block_number: Union[int, None]
    ):
        payload = Request(
            "chain_getAssetSchemeByType", asset_type, shard_id, block_number,
        )
        response = self.client.send(payload)

        return response.data.result

    def get_asset(
        self,
        tracker: str,
        transaction_index: int,
        shrad_id: int,
        block_number: Union[int, None],
    ):
        payload = Request(
            "chain_getAsset", tracker, transaction_index, shrad_id, block_number,
        )
        response = self.client.send(payload)

        return response.data.result

    def get_text(self, transaction_hash: str, block_number: Union[int, None]):
        payload = Request("chain_getText", transaction_hash, block_number)
        response = self.client.send(payload)

        return response.data.result

    def is_asset_spent(
        self,
        tracker: str,
        transaction_index: int,
        shard_id: int,
        block_number: Union[int, None],
    ):
        payload = Request(
            "chain_isAssetSpent", tracker, transaction_index, shard_id, block_number,
        )
        response = self.client.send(payload)

        return response.data.result

    def get_seq(self, address: str, block_number: Union[int, None]):
        payload = Request("chain_getSeq", address, block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_balance(self, address: str, block_number: Union[int, None]):
        payload = Request("chain_getBalance", address, block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_regualr_key(self, address: str, block_number: Union[int, None]):
        payload = Request("chain_getRegularKey", address, block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_regualr_key_owner(self, public_key: str, block_number: Union[int, None]):
        payload = Request("chain_getRegularKeyOwner", public_key, block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_genesis_accounts(self):
        payload = Request("chain_getGenesisAccounts")
        response = self.client.send(payload)

        return response.data.result

    def get_number_of_shards(self, block_number: Union[int, None]):
        payload = Request("chain_getNumberOfShards", block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_shard_id_by_hash(
        self, transaction_hash: str, block_number: Union[int, None]
    ):
        payload = Request("chain_getShardIdByHash", transaction_hash, block_number,)
        response = self.client.send(payload)

        return response.data.result

    def get_shard_root(self, shard_id: int, block_number: Union[int, None]):
        payload = Request("chain_getShardRoot", shard_id, block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_shard_owners(self, shard_id: int, block_number: Union[int, None]):
        payload = Request("chain_getShardOwners", shard_id, block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_shard_users(self, shard_id: int, block_number: Union[int, None]):
        payload = Request("chain_getShardUsers", shard_id, block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_mining_reward(self, block_number: Union[int, None]):
        payload = Request("chain_getMiningReward", block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_min_transaction_fee(
        self, transaction_type: str, block_number: Union[int, None]
    ):
        payload = Request("chain_getMinTransactionFee", transaction_type, block_number,)
        response = self.client.send(payload)

        return response.data.result

    def get_common_params(self, block_number: Union[int, None]):
        payload = Request("chain_getCommonParams", block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_term_metadata(self, block_number: Union[int, None]):
        payload = Request("chain_get_termMetadata", block_number)
        response = self.client.send(payload)

        return response.data.result

    def execute_transaction(self, transaction, sender: str):
        payload = Request("chain_executeTransaction", transaction, sender)
        response = self.client.send(payload)

        return response.data.result

    def execute_vm(
        self, transaction, parameters: List[List[List[int]]], indices: List[List[int]]
    ):
        payload = Request("chain_executeVM", transaction, parameters, indices,)
        response = self.client.send(payload)

        return response.data.result

    def get_network_id(self):
        payload = Request("chain_getNetworkId")
        response = self.client.send(payload)

        return response.data.result

    def get_possible_authors(self, block_number: Union[int, None]):
        payload = Request("chain_getPossibleAuthors", block_number)
        response = self.client.send(payload)

        return response.data.result

    def get_metadata_seq(self, block_number: Union[int, None]):
        payload = Request("chain_getMetadataSeq", block_number)
        response = self.client.send(payload)

        return response.data.result
