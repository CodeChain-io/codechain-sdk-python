import binascii
from dataclasses import dataclass
from typing import List
from typing import Union

from ..key.p2pkh import P2PKH
from ..key.p2pkhburn import P2PKHBurn
from codechain.primitives import AssetAddress
from codechain.primitives import H160
from codechain.primitives import U64


@dataclass
class AssetTransferOutputJSON:
    lock_script_hash: str
    parameters: List[str]
    asset_type: str
    shard_id: int
    quantity: str


class AssetTransferOutput:
    def __init__(
        self,
        asset_type: H160,
        shard_id: int,
        quantity: U64,
        recipient: AssetAddress = None,
        lock_script_hash: H160 = None,
        parameters: bytes = None,
    ):
        if recipient is not None:
            address_type = recipient.address_type
            payload = recipient.payload
            if "pubkeys" in payload:
                raise ValueError("Multisig payload is not supported yet")

            if address_type == 0x00:
                self.lock_script_hash = payload
                self.parameters = []
            elif address_type == 0x01:
                self.lock_script_hash = P2PKH.get_lock_script_hash()
                self.parameters = [bytes(payload)]
            elif address_type == 0x02:
                self.lock_script_hash = P2PKHBurn.get_lock_script_hash()
                self.parameters = [bytes(payload)]
            else:
                raise ValueError(
                    f"Unexpected type of AssetAddress: {address_type}, {recipient}"
                )
        else:
            self.lock_script_hash = lock_script_hash
            self.parameters = parameters

        self.asset_type = asset_type
        self.shard_id = shard_id
        self.quantity = quantity

    @staticmethod
    def from_json(data: AssetTransferOutputJSON):
        return AssetTransferOutput(
            H160(data["lockScriptHash"]),
            map(lambda x: bytes.fromhex(x), data["parameters"]),
            H160(data["assetType"]),
            data["shardId"],
            U64(data["quantity"]),
        )

    def to_encode_object(self):
        return [
            self.lock_script_hash.to_encode_object(),
            map(lambda x: bytes(x), self.parameters),
            self.asset_type.to_encode_object(),
            self.shard_id,
            self.quantity.to_encode_object(),
        ]

    def to_json(self):
        return {
            "lockScriptHash": self.lock_script_hash.to_json(),
            "parameters": map(
                lambda x: binascii.hexlify(x).decode("ascii"), self.parameters
            ),
            "assetType": self.asset_type.to_json(),
            "shardId": self.shard_id,
            "quantity": self.quantity.to_json(),
        }
