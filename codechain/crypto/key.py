from typing import Union

from coincurve import PrivateKey
from coincurve import PublicKey


def generate_private_key():
    """Generates a private key."""
    privkey = PrivateKey()
    return bytes.fromhex(privkey.to_hex())


def get_public_from_private(priv: Union[bytearray, bytes, str]):
    """Gets public key from private key."""

    if isinstance(priv, str):
        priv = bytes.fromhex(priv)

    privkey = PrivateKey(priv)
    return privkey.public_key.format(compressed=False)[1:]
