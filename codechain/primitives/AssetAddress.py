import re
from dataclasses import dataclass
from typing import List
from typing import Union

from ..crypto import bech32_decode
from ..crypto import bech32_encode
from .HexString import H160


@dataclass
class MultiSig:
    n: int
    m: int
    pubkeys: List[H160]


class AssetAddress:
    def __init__(
        self, address_type: int, payload: Union[H160, str, MultiSig], address: str
    ):
        self.address_type = address_type

        if isinstance(payload, (H160, str)):
            self.payload = H160(payload)
        else:
            n, m, pubkeys = payload
            self.payload = (n, m, list(map(lambda p: H160(p), pubkeys)))
        self.value = address

    @staticmethod
    def from_type_and_payload(
        network_type: int, payload: Union[H160, str, MultiSig], **kwargs
    ):
        network_id = kwargs.get("network_id", "cc")
        version = kwargs.get("version", 1)

        if version != 1:
            raise ValueError(f"Unsupported version for asset address: {version}")
        if network_type < 0x00 or network_type > 0x03:
            raise ValueError(f"Unsupported type for asset address: {network_type}")

        address = bech32_encode(
            network_id + "a", bytes([version, network_type]) + encode_payload(payload)
        )

        return AssetAddress(network_type, payload, address)

    @staticmethod
    def from_string(address: str):
        if address[2] != "a":
            raise ValueError(f"The prefix is unknown for asset address: {address}")

        byte = bech32_decode(address[:3], address)
        version = byte[0]

        if version != 1:
            raise ValueError(f"Unsupported version for asset address: {address}")

        address_type = byte[1]

        if address_type < 0x0 or address_type > 0x3:
            raise ValueError(f"Unsupported type for asset address: {address}")

        if address_type < 0x3:
            payload = H160(byte[2:])
            return AssetAddress(address_type, payload, address)
        else:
            n = byte[2]
            m = byte[3]
            payload = byte[4:]
            pubkeys = []
            if len(payload) % 20 != 0:
                raise ValueError(
                    f"Invalid pubkeys length which should be a multiple of 20 but {len(payload)}"
                )
            for i in range(0, len(payload), 20):
                pubkeys.append(H160(payload[i : i + 20]))

            return AssetAddress(address_type, MultiSig(n, m, pubkeys), address)

    @staticmethod
    def check(address):
        return (
            True
            if isinstance(address, AssetAddress)
            else AssetAddress.check_string(address)
        )

    @staticmethod
    def check_string(address: str):
        return None is not re.match(
            "^.{2}a[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{42}$", address
        )

    @staticmethod
    def ensure(address):
        return (
            address
            if isinstance(address, AssetAddress)
            else AssetAddress.from_string(address)
        )

    def __str__(self) -> str:
        return self.value

    def __eq__(self, rhs_value):
        return self.value == rhs_value.value

    def __hash__(self):
        return hash(self.value)


def encode_payload(payload: Union[H160, str, MultiSig]) -> bytes:
    if isinstance(payload, (H160, str)):
        return H160(payload)
    else:
        n, m, pubkeys = payload
        return bytes([n, m]) + b"".join(map(lambda p: H160(p), pubkeys))
