import pytest

from codechain.crypto import generate_private_key
from codechain.keystore import decode
from codechain.keystore import encode
from codechain.keystore import hd_decode
from codechain.keystore import hd_encode
from codechain.keystore import KeyType


def test_storage_encoding():
    private_key = generate_private_key()
    storage = encode(private_key, KeyType.ASSET, "passphrase", "metadata")
    private = decode(storage, "passphrase")

    assert private_key == bytes.fromhex(private)


def test_hd_storage_encoding():
    seed = b"00" * 32
    storage = hd_encode(seed, "passphrase", "metadata")
    result_seed = hd_decode(storage, "passphrase")

    assert seed == bytes.fromhex(result_seed)
