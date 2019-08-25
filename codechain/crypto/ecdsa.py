from coincurve import PrivateKey
from coincurve import PublicKey
from coincurve import verify_signature

SECPK1_N = (
    115792089237316195423570985008687907852837564279074904382605163141518161494337
)


def sign_ecdsa(message, priv):
    """Gets ECDSA signature for message from private key."""

    if not isinstance(message, (bytes, bytearray)):
        raise TypeError(f"Invalid message")
    if len(message) != 32:
        raise ValueError(f"Invalid length message: {len(message)} != 32")
    if not isinstance(priv, (bytes, bytearray)):
        raise TypeError(f"Invalid private key")
    if len(priv) != 32:
        raise ValueError(f"Invalid length private key: {len(priv)} != 32")

    privkey = PrivateKey(priv)
    sig_check = privkey.sign_recoverable(message, hasher=None)

    return sig_check


def verify_ecdsa(message, signature, pub):
    """Checks if the signature from signEcdsa is correct."""

    if not isinstance(message, (bytes, bytearray)):
        raise TypeError(f"Invalid message")
    if len(message) != 32:
        raise ValueError(f"Invalid length message: {len(message)} != 32")
    if not isinstance(signature, (bytes, bytearray)):
        raise TypeError(f"Invalid signature key")
    if len(signature) != 65:
        raise ValueError(f"Invalid length signature key: {len(signature)} != 65")
    if not isinstance(pub, (bytes, bytearray)):
        raise TypeError(f"Invalid signature key")
    if len(pub) != 64:
        raise ValueError(f"Invalid length signature key: {len(pub)} != 64")

    pubkey = PublicKey(b"\x04" + pub)

    r = _big_endian_to_int(signature[0:32])
    s = _big_endian_to_int(signature[32:64])

    low_s = _coerce_low_s(s)
    der_encoded_signature = bytes(_two_int_sequence_encoder(r, low_s))

    return verify_signature(
        der_encoded_signature, message, pubkey.format(compressed=False), hasher=None
    )


def recover_ecdsa(message, signature):
    """Gets public key from the message and ECDSA signature."""

    if not isinstance(message, (bytes, bytearray)):
        raise TypeError(f"Invalid message")
    if len(message) != 32:
        raise ValueError(f"Invalid length message: {len(message)} != 32")
    if not isinstance(signature, (bytes, bytearray)):
        raise TypeError(f"Invalid signature key")
    if len(signature) != 65:
        raise ValueError(f"Invalid length signature key: {len(signature)} != 65")

    return PublicKey.from_signature_and_message(signature, message, hasher=None).format(
        compressed=False
    )[1:]


def _int_to_big_endian(value: int) -> bytes:
    return value.to_bytes((value.bit_length() + 7) // 8 or 1, "big")


def _big_endian_to_int(value: bytes) -> int:
    return int.from_bytes(value, "big")


def _coerce_low_s(value: int) -> int:
    """Coerce the s component of an ECDSA signature into its low-s form.

    See https://bitcoin.stackexchange.com/questions/83408/in-ecdsa-why-is-r-%E2%88%92s-mod-n-complementary-to-r-s  # noqa: W501
    or https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2.md.
    """
    return min(value, -value % SECPK1_N)


def _encode_int(primitive: int):
    # See: https://docs.microsoft.com/en-us/windows/desktop/seccertenroll/about-integer

    # Integer tag
    yield 0x02

    encoded = _int_to_big_endian(primitive)
    if encoded[0] >= 128:
        # Indicate that integer is positive
        yield len(encoded) + 1
        yield 0x00
    else:
        yield len(encoded)

    yield from encoded


def _two_int_sequence_encoder(signature_r: int, signature_s: int):
    """
    Encode two integers using DER, defined as:

    ::

        ECDSASpec DEFINITIONS ::= BEGIN
              ECDSASignature ::= SEQUENCE {
                 r   INTEGER,
                 s   INTEGER
             }
        END

    Only a subset of integers are supported: positive, 32-byte ints.

    See: https://docs.microsoft.com/en-us/windows/desktop/seccertenroll/about-sequence
    """
    # Sequence tag
    yield 0x30

    encoded1 = bytes(_encode_int(signature_r))
    encoded2 = bytes(_encode_int(signature_s))

    # Sequence length
    yield len(encoded1) + len(encoded2)

    yield from encoded1
    yield from encoded2
