from typing import List
from typing import Union

from jsonrpcclient.requests import Request


class Chain:
    def __init__(self, client):
        self.client = client

    def get_block_number(self):
        payload = Request("chain_getBestBlocknumber")
        response = self.client.send(payload)

        return response.result

    def get_best_block_id(self):
        payload = Request("chain_getBestBlockId")
        response = self.client.send(payload)

        return response.result

    def get_block_hash(self, block_number: Union[int, None]):
        payload = Request("chain_getBlockHash", blockNumber=block_number)
        response = self.client.send(payload)

        return response.result

    def get_block_by_number(self, block_number: Union[int, None]):
        payload = Request("chain_getBlockByNumber", blockNumber=block_number)
        response = self.client.send(payload)

        return response.result

    def get_block_by_hash(self, block_hash: str):
        payload = Request("chain_getBlockByHash", blockHash=block_hash)
        response = self.client.send(payload)

        return response.result

    def get_block_transaction_count_by_hash(self, block_hash: str):
        payload = Request("chain_getBlockTransactionCountByHash", blockHash=block_hash)
        response = self.client.send(payload)

        return response.result

    def get_transaction(self, transaction_hash: str):
        payload = Request("chain_getTransaction", transactionHash=transaction_hash)
        response = self.client.send(payload)

        return response.result

    def get_transaction_signer(self, transaction_hash: str):
        payload = Request(
            "chain_getTransactionSigner", transactionHash=transaction_hash
        )
        response = self.client.send(payload)

        return response.result

    def contains_transaction(self, transaction_hash: str):
        payload = Request("chain_containsTransaction", transactionHash=transaction_hash)
        response = self.client.send(payload)

        return response.result

    def get_transaction_by_tracker(self, tracker: str):
        payload = Request("chain_getTransactionByTracker", tracker=tracker)
        response = self.client.send(payload)

        return response.result

    def get_asset_scheme_by_tracker(
        self, tracker: str, shard_id: int, block_number: Union[int, None]
    ):
        payload = Request(
            "chain_getAsset_schemeByTracker",
            tracker=tracker,
            shardId=shard_id,
            blockNumber=block_number,
        )
        response = self.client.send(payload)

        return response.result

    def get_asset_scheme_by_type(
        self, asset_type: str, shard_id: int, block_number: Union[int, None]
    ):
        payload = Request(
            "chain_getAssetSchemeByType",
            assetType=asset_type,
            shardId=shard_id,
            blockNumber=block_number,
        )
        response = self.client.send(payload)

        return response.result

    def get_asset(
        self,
        tracker: str,
        transaction_index: int,
        shrad_id: int,
        block_number: Union[int, None],
    ):
        payload = Request(
            "chain_getAsset",
            tracker=tracker,
            transactionIndex=transaction_index,
            shardId=shrad_id,
            blockNumber=block_number,
        )
        response = self.client.send(payload)

        return response.result

    def get_text(self, transaction_hash: str, block_number: Union[int, None]):
        payload = Request(
            "chain_getText", transactionHash=transaction_hash, blockNumber=block_number
        )
        response = self.client.send(payload)

        return response.result

    def is_asset_spent(
        self,
        tracker: str,
        transaction_index: int,
        shard_id: int,
        block_number: Union[int, None],
    ):
        payload = Request(
            "chain_isAssetSpent",
            tracker=tracker,
            transactionIndex=transaction_index,
            shardId=shard_id,
            blockNumber=block_number,
        )
        response = self.client.send(payload)

        return response.result

    def get_seq(self, address: str, block_number: Union[int, None]):
        payload = Request("chain_getSeq", address=address, blockNumber=block_number)
        response = self.client.send(payload)

        return response.result

    def get_balance(self, address: str, block_number: Union[int, None]):
        payload = Request("chain_getBalance", address=address, blockNumber=block_number)
        response = self.client.send(payload)

        return response.result

    def get_regualr_key(self, address: str, block_number: Union[int, None]):
        payload = Request(
            "chain_getRegularKey", address=address, blockNumber=block_number
        )
        response = self.client.send(payload)

        return response.result

    def get_regualr_key_owner(self, public_key: str, block_number: Union[int, None]):
        payload = Request(
            "chain_getRegularKeyOwner", publicKey=public_key, blockNumber=block_number
        )
        response = self.client.send(payload)

        return response.result

    def get_genesis_accounts(self):
        payload = Request("chain_getGenesisAccounts")
        response = self.client.send(payload)

        return response.result

    def get_number_of_shards(self, block_number: Union[int, None]):
        payload = Request("chain_getNumberOfShards", blockNumber=block_number)
        response = self.client.send(payload)

        return response.result

    def get_shard_id_by_hash(
        self, transaction_hash: str, block_number: Union[int, None]
    ):
        payload = Request(
            "chain_getShardIdByHash",
            transactionHash=transaction_hash,
            blockNumber=block_number,
        )
        response = self.client.send(payload)

        return response.result

    def get_shard_root(self, shard_id: int, block_number: Union[int, None]):
        payload = Request(
            "chain_getShardRoot", shardId=shard_id, blockNumber=block_number
        )
        response = self.client.send(payload)

        return response.result

    def get_shard_owners(self, shard_id: int, block_number: Union[int, None]):
        payload = Request(
            "chain_getShardOwners", shardId=shard_id, blockNumber=block_number
        )
        response = self.client.send(payload)

        return response.result

    def get_shard_users(self, shard_id: int, block_number: Union[int, None]):
        payload = Request(
            "chain_getShardUsers", shardId=shard_id, blockNumber=block_number
        )
        response = self.client.send(payload)

        return response.result

    def get_mining_reward(self, block_number: Union[int, None]):
        payload = Request("chain_getMiningReward", blockNumber=block_number)
        response = self.client.send(payload)

        return response.result

    def get_min_transaction_fee(
        self, transaction_type: str, block_number: Union[int, None]
    ):
        payload = Request(
            "chain_getMinTransactionFee",
            transactionType=transaction_type,
            blockNumber=block_number,
        )
        response = self.client.send(payload)

        return response.result

    def get_common_params(self, block_number: Union[int, None]):
        payload = Request("chain_getCommonParams", blockNumber=block_number)
        response = self.client.send(payload)

        return response.result

    def get_term_metadata(self, block_number: Union[int, None]):
        payload = Request("chain_get_termMetadata", blockNumber=block_number)
        response = self.client.send(payload)

        return response.result

    def execute_transaction(self, transaction, sender: str):
        payload = Request(
            "chain_executeTransaction", transaction=transaction, sender=sender
        )
        response = self.client.send(payload)

        return response.result

    def execute_vm(
        self, transaction, parameters: List[List[List[int]]], indices: List[List[int]]
    ):
        payload = Request(
            "chain_executeVM",
            transaction=transaction,
            parameters=parameters,
            indices=indices,
        )
        response = self.client.send(payload)

        return response.result

    def get_network_id(self):
        payload = Request("chain_getNetworkId")
        response = self.client.send(payload)

        return response.result

    def get_possible_authors(self, block_number: Union[int, None]):
        payload = Request("chain_getPossibleAuthors", blockNumber=block_number)
        response = self.client.send(payload)

        return response.result

    def get_metadata_seq(self, block_number: Union[int, None]):
        payload = Request("chain_getMetadataSeq", blockNumber=block_number)
        response = self.client.send(payload)

        return response.result
