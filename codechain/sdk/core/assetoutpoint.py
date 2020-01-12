import binascii
from dataclasses import dataclass
from typing import List
from typing import Union

from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import U64


@dataclass
class AssetOutPointJSON:
    tracker: str
    index: int
    asset_type: str
    shard_id: int
    quantity: str
    lock_script_hash: Union[None, str]
    parameters: List[bytes]


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
    def from_json(data: AssetOutPointJSON):
        return AssetOutPoint(
            H256(data.tracker),
            data.index,
            H160(data.asset_type),
            data.shard_id,
            U64(data.quantity),
            None if data.lock_script_hash is None else H160(data.lock_script_hash),
            None
            if data.parameters is None
            else list(map(lambda x: bytes.fromhex(x), data.parameters)),
        )

    def to_encode_object(self):
        return [
            self.tracker.to_encode_object(),
            self.index,
            self.asset_type.to_encode_object(),
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
            else list(
                map(lambda x: binascii.hexlify(x).decode("ascii"), self.parameters)
            ),
        }
