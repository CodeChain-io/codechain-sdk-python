from coincurve import PrivateKey, PublicKey
# Generates a private key.


def generate_private_key():
    privkey = PrivateKey()
    return bytes(bytearray.fromhex(privkey.to_hex()))


# Gets public key from private key.


def get_public_from_private(priv: bytes):
    privkey=PrivateKey(priv)
    return privkey.public_key.format(compressed=False)[1:]
