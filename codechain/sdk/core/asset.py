import binascii
from dataclasses import dataclass
from typing import List
from typing import Union

from .assetoutpoint import AssetOutPoint
from .assettransferinput import AssetTransferInput
from .assettransferinput import Timelock
from codechain.primitives import AssetAddress
from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import U64


@dataclass
class AssetJSON:
    asset_type: str
    lock_script_hash: str
    parameters: List[str]
    quantity: str
    order_hash: Union[str, None]
    shard_id: int
    tracker: str
    transaction_output_index: int


class Asset:
    def __init__(
        self,
        tracker: H256,
        transaction_output_index: int,
        asset_type: H160,
        shard_id: int,
        quantity: U64,
        lock_script_hash: H160,
        parameters: List[bytes],
        order_hash=None,
    ):
        self.asset_type = asset_type
        self.shard_id = shard_id
        self.lock_script_hash = lock_script_hash
        self.parameters = parameters
        self.quantity = quantity
        self.order_hash = order_hash
        self.out_point = AssetOutPoint(
            tracker,
            transaction_output_index,
            asset_type,
            shard_id,
            quantity,
            lock_script_hash,
            parameters,
        )

    @staticmethod
    def from_json(data):
        return Asset(
            H256(data["tracker"]),
            data["transactionOutputIndex"],
            H160(data["assetType"]),
            data["shardId"],
            U64(data["quantity"]),
            H160(data["lockScriptHash"]),
            map(lambda x: bytes.fromhex(x), data["parameters"]),
            None if data["orderHash"] is None else H256(data["orderHash"]),
        )

    def to_json(self):
        tracker = self.out_point.tracker
        index = self.out_point.index

        return {
            "assetType": self.asset_type.to_json(),
            "shardId": self.shard_id,
            "lockScriptHash": self.lock_script_hash.to_json(),
            "parameters": map(
                lambda x: binascii.hexlify(x).decode("ascii"), self.parameters
            ),
            "quantity": self.quantity.to_json(),
            "orderHash": None if self.order_hash is None else self.order_hash.to_json(),
            "tracker": tracker.to_json(),
            "transactionOutputIndex": index,
        }

    def create_transfer_input(self, timelock: Union[Timelock, None] = None):
        return AssetTransferInput(self.out_point, timelock)

    def create_transfer_transaction(
        self,
        network_id: str,
        recipient: List = None,
        timelock: Union[Timelock, None] = None,
        metadata="",
        approvals: List[str] = None,
        expiration: int = None,
    ):
        if recipient is None:
            recipient = []
        if approvals is None:
            approvals = []

        from .assettransferoutput import AssetTransferOutput
        from .transferasset import TransferAsset
        return TransferAsset(
            [],
            [AssetTransferInput(self.out_point, timelock, bytes(), bytes())],
            map(
                lambda x: AssetTransferOutput(
                    self.asset_type,
                    self.shard_id,
                    x.quantity,
                    AssetAddress.ensure(x.address),
                ),
                recipient,
            ),
            [],
            network_id,
            metadata,
            approvals,
            expiration,
        )
