import binascii
import re

import pytest

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


@pytest.mark.parametrize(
    "priv_str, pub_str",
    [
        (
            "3d4efd662b35b8d459006442f94e692d1031fc45e95c64d093a2309afb86d8a5",
            "68153506fd5c7a504692de13e0c78baaa3ba9ac41a601fa3ac32918f280e6c3818887a52d46900484c00ddbedd197ec6d2a170b04f7ac084a1e6d39802d8ad67",
        ),
        (
            "5f7e4b49bb13b2d9464f5910bbf688c03a885000f695dbd5d5a4ab09dfeb0408",
            "9288d69533be9ef941cdda18c94a2bd6f41ba2fc6d556e6fad5655038703d9ea51ad216c1a163f0449b76e758f01663a84d748e4194df0d7ca07e524a6e9d985",
        ),
        (
            "4380f52f37e3360ba47919a3d752b53e45756a59e6e0652bcdfee576454ea6e3",
            "c82d697660f6da7de71359dd288021f139b61772ab3e77dcc8d785c7abbc8d01fe2a074a67318e1c618e4c76a9ad1a1aa38e9785f3eb6dcc9aa3d1c785fbd141",
        ),
    ],
)
def test_get_public_from_private_example(priv_str, pub_str):
    priv = bytes.fromhex(priv_str)
    pub = bytes.fromhex(pub_str)

    generated_pub = get_public_from_private(priv)

    assert generated_pub == pub
