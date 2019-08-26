import binascii
import re

from codechain.crypto import generate_private_key
from codechain.crypto import get_public_from_private


def test_generate_private_key():
    priv = generate_private_key()
    assert (
        re.match("^[0-9a-fA-F]{64}$", binascii.hexlify(priv).decode("ascii"))
        is not None
    )


def test_get_public_from_private():
    priv = generate_private_key()
    pub = get_public_from_private(priv)

    assert (
        re.match("^[0-9a-fA-F]{128}$", binascii.hexlify(pub).decode("ascii"))
        is not None
    )
