import binascii
from dataclasses import dataclass
from typing import List

from rlp import encode

from ..key.p2pkh import P2PKH
from ..key.p2pkhburn import P2PKHBurn
from ..utils import blake256
from .assetoutpoint import AssetOutPoint
from .assetoutpoint import AssetOutPointJSON
from codechain.primitives import AssetAddress
from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import U64


@dataclass
class OrderJSON:
    asset_type_from: str
    asset_type_to: str
    asset_type_fee: str
    shard_id_from: int
    shard_id_to: int
    shard_id_fee: int
    asset_quantity_from: str
    asset_quantity_to: str
    asset_quantity_fee: str
    origin_outputs: List[AssetOutPointJSON]
    expiration: str
    lock_script_hash_from: str
    parameters_from: List[str]
    lock_script_hash_fee: str
    parameters_fee: List[str]


@dataclass
class OrderDataBasic:
    asset_type_from: H160
    asset_type_to: H160
    asset_type_fee: H160
    shard_id_from: int
    shard_id_to: int
    shard_id_fee: int
    asset_quantity_from: U64
    asset_quantity_to: U64
    asset_quantity_fee: U64
    origin_outputs: List[AssetOutPoint]
    expiration: U64


class Order:
    def __init__(
        self,
        asset_type_from: H160,
        asset_type_to: H160,
        asset_type_fee: H160,
        shard_id_from: int,
        shard_id_to: int,
        shard_id_fee: int,
        asset_quantity_from: U64,
        asset_quantity_to: U64,
        asset_quantity_fee: U64,
        origin_outputs: List[AssetOutPoint],
        expiration: U64,
        lock_script_hash_from: H160 = None,
        parameters_from: List[bytes] = None,
        recipient_from: AssetAddress = None,
        lock_script_hash_fee: H160 = None,
        parameters_fee: List[bytes] = None,
        recipient_fee: AssetAddress = None,
    ):
        if recipient_from is not None:
            self.lock_script_hash_from, self.parameters_from = decompose_recipient(
                recipient_from
            )
        else:
            if lock_script_hash_from is None or parameters_from is None:
                raise ValueError("recipient_from should not be None")
            self.lock_script_hash_from = lock_script_hash_from
            self.parameters_from = parameters_from

        if recipient_fee is not None:
            self.lock_script_hash_fee, self.parameters_fee = decompose_recipient(
                recipient_fee
            )
        else:
            if lock_script_hash_fee is None or parameters_fee is None:
                raise ValueError("recipient_fee should not be None")
            self.lock_script_hash_fee = lock_script_hash_fee
            self.parameters_fee = parameters_fee

        self.asset_type_from = asset_type_from
        self.asset_type_to = asset_type_to
        self.asset_type_fee = (
            H160(H160.ZERO) if asset_type_fee is None else asset_type_fee
        )
        self.shard_id_from = shard_id_from
        self.shard_id_to = shard_id_to
        self.shard_id_fee = 0 if shard_id_fee is None else shard_id_fee
        self.asset_quantity_from = asset_quantity_from
        self.asset_quantity_to = asset_quantity_to
        self.asset_quantity_fee = (
            U64(0) if asset_quantity_fee is None else asset_quantity_fee
        )
        self.origin_outputs = origin_outputs
        self.expiration = expiration

        asset_quantity_from_is_zero = asset_quantity_from == 0
        asset_quantity_to_is_zero = asset_quantity_to == 0
        asset_quantity_fee_is_zero = asset_quantity_fee == 0

        if asset_type_from == asset_type_to and shard_id_from == shard_id_to:
            raise ValueError(
                f"assetTypeFrom and assetTypeTo is same: {asset_type_from}(shard {shard_id_from})"
            )
        elif not asset_quantity_fee_is_zero:
            if asset_type_from == asset_type_fee and shard_id_from == shard_id_fee:
                raise ValueError(
                    f"assetTypeFrom and assetTypeFee is same: {asset_type_from}(shard {shard_id_from})"
                )
            if asset_type_to == asset_type_fee and shard_id_to == shard_id_fee:
                raise ValueError(
                    f"assetTypeTo and assetTypeFee is same: {asset_type_to}(shard {shard_id_to})"
                )

        if (
            (asset_quantity_from_is_zero and not asset_quantity_to_is_zero)
            or (not asset_quantity_from_is_zero and asset_quantity_to_is_zero)
            or (asset_quantity_from_is_zero and asset_quantity_fee_is_zero)
            or (
                not asset_quantity_from_is_zero
                and not (asset_quantity_fee % asset_quantity_from) == 0
            )
        ):
            raise ValueError(
                f"The given quantity ratio is invalid: {asset_quantity_from}:{asset_quantity_to}:{asset_quantity_fee}"
            )

        if len(origin_outputs) == 0:
            raise ValueError(f"originOutputs is empty")

    @staticmethod
    def from_json(data: OrderJSON):
        return Order(
            H160(data["assetTypeFrom"]),
            H160(data["assetTypeTo"]),
            H160(data["assetTypeFee"]),
            data["shardIdFrom"],
            data["shardIdTo"],
            data["shardIdFee"],
            U64(data["assetQuantityFrom"]),
            U64(data["assetQuantityTo"]),
            U64(data["assetQuantityFee"]),
            list(map(lambda x: AssetOutPoint.from_json(x), data["originOutputs"])),
            U64(data["expiration"]),
            H160(data["lockScriptHashFrom"]),
            list(map(lambda x: bytes.fromhex(x), data["parametersFrom"])),
            H160(data["lockSCriptHashFee"]),
            list(map(lambda x: bytes.fromhex(x), data["parametersFee"])),
        )

    def to_encode_object(self):
        return [
            self.asset_type_from.to_encode_object(),
            self.asset_type_to.to_encode_object(),
            self.asset_type_fee.to_encode_object(),
            self.shard_id_from,
            self.shard_id_to,
            self.shard_id_fee,
            self.asset_quantity_from.to_encode_object(),
            self.asset_quantity_to.to_encode_object(),
            self.asset_quantity_fee.to_encode_object(),
            list(map(lambda x: x.to_encode_object(), self.origin_outputs)),
            self.expiration.to_encode_object(),
            self.lock_script_hash_from.to_encode_object(),
            list(map(lambda x: bytes(x), self.parameters_from)),
            self.lock_script_hash_fee.to_encode_object(),
            list(map(lambda x: bytes(x), self.parameters_fee)),
        ]

    def rlp_bytes(self):
        return encode(self.to_encode_object())

    def to_json(self):
        return {
            "assetTypeFrom": self.asset_type_from.to_json(),
            "assetTypeTo": self.asset_type_from.to_json(),
            "assetTypeFee": self.asset_type_fee.to_json(),
            "shardIdFrom": self.shard_id_from,
            "shardIdTo": self.shard_id_to,
            "shardIdFee": self.shard_id_fee,
            "assetQuantityFrom": self.asset_quantity_from.to_json(),
            "assetQuantityTo": self.asset_quantity_to.to_json(),
            "assetQuantityFee": self.asset_quantity_fee.to_json(),
            "originOutputs": list(map(lambda x: x.to_json(), self.origin_outputs)),
            "expiration": str(self.expiration),
            "lockScriptHashFrom": self.lock_script_hash_from.to_json(),
            "parametersFrom": list(
                map(lambda x: binascii.hexlify(x).decode("ascii"), self.parameters_from)
            ),
            "lockScriptHashFee": self.lock_script_hash_fee.to_json(),
            "parametersFee": list(
                map(lambda x: binascii.hexlify(x).decode("ascii"), self.parameters_fee)
            ),
        }

    def hash(self):
        return H256(blake256(self.rlp_bytes()))

    def consume(self, quantity: U64):
        quantity_from = U64(quantity)
        if quantity_from > self.asset_quantity_from:
            raise ValueError(
                f"The given quantity is too big: {quantity_from} > {self.asset_quantity_from}"
            )

        remain_quantity_from = self.asset_quantity_from - quantity_from
        if not (
            ((remain_quantity_from * self.asset_quantity_to) % self.asset_quantity_from)
            == 0
        ):
            raise ValueError(
                f"The given quantity does not fit to the ratio: {self.asset_quantity_from}:{self.asset_quantity_to}"
            )

        remain_quantity_to = (
            remain_quantity_from * self.asset_quantity_to / self.asset_quantity_from
        )
        remain_quantity_fee = (
            remain_quantity_from * self.asset_quantity_fee / self.asset_quantity_from
        )

        return Order(
            self.asset_type_from,
            self.asset_type_to,
            self.asset_type_fee,
            self.shard_id_from,
            self.shard_id_to,
            self.shard_id_fee,
            U64(remain_quantity_from),
            U64(remain_quantity_to),
            U64(remain_quantity_fee),
            self.origin_outputs,
            self.expiration,
            self.lock_script_hash_from,
            self.parameters_from,
            self.lock_script_hash_fee,
            self.parameters_fee,
        )


def decompose_recipient(recipient: AssetAddress):
    address_type = recipient.address_type
    payload = recipient.payload

    if "pubkeys" in payload:
        raise ValueError("Multisig payload is not supported yet")

    if address_type == 0x00:
        return payload, []
    elif address_type == 0x01:
        return P2PKH.get_lock_script_hash(), [bytes(payload)]
    elif address_type == 0x02:
        return P2PKHBurn.get_lock_script_hash(), [bytes(payload)]
    else:
        raise ValueError(
            f"Unexpected type of AssetAddress: {address_type}, {recipient}"
        )
