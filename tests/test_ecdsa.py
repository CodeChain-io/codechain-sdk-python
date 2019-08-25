import pytest
from coincurve.utils import der_to_pem

from codechain.crypto import generate_private_key
from codechain.crypto import get_public_from_private
from codechain.crypto import recover_ecdsa
from codechain.crypto import sign_ecdsa
from codechain.crypto import verify_ecdsa


def test_sign_verify():
    message = bytes(32)
    priv = generate_private_key()
    pub = get_public_from_private(priv)
    sig = sign_ecdsa(message, priv)

    assert verify_ecdsa(message, sig, pub)
