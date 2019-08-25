from coincurve import PrivateKey
from coincurve import PublicKey


def generate_private_key():
    """Generates a private key."""
    privkey = PrivateKey()
    return bytes(bytearray.fromhex(privkey.to_hex()))


def get_public_from_private(priv: bytes):
    """Gets public key from private key."""
    privkey = PrivateKey(priv)
    return privkey.public_key.format(compressed=False)[1:]
