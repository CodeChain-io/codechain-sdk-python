import binascii

from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import U64


class AssetOutPoint:
    def __init__(
        self,
        tracker: H256,
        index: int,
        asset_type: H160,
        shard_id: int,
        quantity: U64,
        lock_script_hash: H160 = None,
        paramters: bytes = None,
    ):
        self.tracker = tracker
        self.index = index
        self.asset_type = asset_type
        self.shard_id = shard_id
        self.quantity = quantity
        self.lock_script_hash = lock_script_hash
        self.parameters = paramters

    @staticmethod
    def from_json(data):
        return AssetOutPoint(
            H256(data["tracker"]),
            data["index"],
            H160(data["assetType"]),
            data["shardId"],
            U64(data["quantity"]),
            None if data["lockScriptHash"] is None else H160(data["lockScriptHash"]),
            None
            if data["parameters"] is None
            else map(lambda x: bytes.fromhex(x), data["paramters"]),
        )

    def to_encode_object(self):
        return [
            self.tracker.to_encoded_object(),
            self.index,
            self.asset_type.to_encoded_object(),
            self.shard_id,
            self.quantity.to_encode_object(),
        ]

    def to_json(self):
        return {
            "tracker": self.tracker.to_json(),
            "index": self.index,
            "assetType": self.asset_type.to_json(),
            "shardId": self.shard_id,
            "quantity": self.quantity.to_json(),
            "lockScriptHash": None
            if self.lock_script_hash is None
            else self.lock_script_hash.to_json(),
            "parameters": None
            if self.parameters is None
            else map(lambda x: binascii.hexlify(x).decode("ascii"), self.parameters),
        }
