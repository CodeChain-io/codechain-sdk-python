import re
from dataclasses import dataclass

from ..crypto import bech32_decode
from ..crypto import bech32_encode
from ..crypto import blake160
from .HexString import H160
from .HexString import H512


@dataclass
class PlatformAddress:
    account_id: H160
    value: str

    @staticmethod
    def from_public(public_key, **kwargs):
        if not H512.check(public_key):
            raise ValueError(
                f"Invalid public key for creating PlatformAddress: {public_key}"
            )

        return PlatformAddress.from_account_id(
            get_account_id_from_public(public_key), **kwargs
        )

    @staticmethod
    def from_account_id(account_id: H160, **kwargs):
        network_id = kwargs.get("network_id", "cc")
        version = int(kwargs.get("version", "1"))

        if not H160.check(account_id):
            raise ValueError(
                f"Invalid account_id for creating PlatformAddress: {account_id}"
            )
        if version != 1:
            raise ValueError(f"Unsupported version for PlatformAddress: {version}")
        if not isinstance(network_id, str) or len(network_id) != 2:
            raise ValueError(
                f"Unsupported network_id for PlatformAddress: {network_id}"
            )

        return PlatformAddress(
            account_id, bech32_encode(network_id + "c", bytes([version]) + account_id)
        )

    @staticmethod
    def from_string(address: str):
        if not isinstance(address, str):
            raise ValueError(f"Expected PlatformAddress string but found: {address}")
        elif address[2] != "c":
            raise ValueError(f"Unknown prefix for PlatformAddress: {address}")

        byte = bech32_decode(address[:3], address)
        version = byte[0]

        if version != 1:
            raise ValueError(f"Unsupported version for PlatformAddress: {version}")

        account_id = H160(byte[1:])

        return PlatformAddress(account_id, address)

    @staticmethod
    def check(address):
        return (
            True
            if isinstance(address, PlatformAddress)
            else PlatformAddress.check_string(address)
        )

    @staticmethod
    def ensure(address):
        if isinstance(address, PlatformAddress):
            return address
        elif isinstance(address, str):
            return PlatformAddress.from_string(address)
        else:
            raise ValueError(
                f"Expected either PlatformAddress or string but found {address}"
            )

    @staticmethod
    def check_string(value: str):
        return None is not re.match(
            "^.{2}c[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{40}$", value
        )

    def __str__(self):
        return self.value


def get_account_id_from_public(public_key):
    return blake160(public_key)
