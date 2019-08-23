from coincurve import PrivateKey
from coincurve import PublicKey
from coincurve import verify_signature


# Gets ECDSA signature for message from private key.
def sign_ecdsa(message, priv):
    if not isinstance(message, (bytes, bytearray)):
        raise TypeError(f"Invalid message: {message}")
    if len(message) != 32:
        raise ValueError(f"Invalid length message: {len(message)} != 32")
    if not isinstance(priv, (bytes, bytearray)):
        raise TypeError(f"Invalid private key: {priv}")
    if len(priv) != 32:
        raise ValueError(f"Invalid length private key: {len(priv)} != 32")

    privkey = PrivateKey(priv)
    sig_check = privkey.sign_recoverable(message, hasher=None)

    return sig_check


# Checks if the signature from signEcdsa is correct.


def verify_ecdsa(message, signature, pub):
    if not isinstance(message, (bytes, bytearray)):
        raise TypeError(f"Invalid message: {message}")
    if len(message) != 32:
        raise ValueError(f"Invalid length message: {len(message)} != 32")
    if not isinstance(signature, (bytes, bytearray)):
        raise TypeError(f"Invalid signature key: {signature}")
    if len(signature) != 65:
        raise ValueError(
            f"Invalid length signature key: {len(signature)} != 65")
    if not isinstance(pub, (bytes, bytearray)):
        raise TypeError(f"Invalid signature key: {pub}")
    if len(pub) != 64:
        raise ValueError(f"Invalid length signature key: {len(pub)} != 64")

    pubkey = PublicKey(b"\x04" + pub)

    return verify_signature(
        signature, message, pubkey.format(compressed=False), hasher=None
    )


# Gets public key from the message and ECDSA signature.


def recover_ecdsa(message, signature):


if not isinstance(message, (bytes, bytearray)):
        raise TypeError(f"Invalid message: {message}")
    if len(message) != 32:
        raise ValueError(f"Invalid length message: {len(message)} != 32")
    if not isinstance(signature, (bytes, bytearray)):
        raise TypeError(f"Invalid signature key: {signature}")
    if len(signature) != 65:
        raise ValueError(f"Invalid length signature key: {len(signature)} != 65")
    return PublicKey.from_signature_and_message(
        signature,
        message,
        hasher=None,
    ).format(compressed=False)[1:]
