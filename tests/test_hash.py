import pytest

from codechain.crypto import blake128
from codechain.crypto import blake128_with_key
from codechain.crypto import blake160
from codechain.crypto import blake160_with_key
from codechain.crypto import blake256
from codechain.crypto import blake256_with_key
from codechain.crypto import ripemd160


@pytest.mark.parametrize("value", ["deadbeef"])
def test_blake128(value):
    result = blake128(value)
    assert result.hex() == "6f5ca1fbef92681581176e231a9ff125"


@pytest.mark.parametrize("value", ["deadbeef"])
def test_blake128_with_key(value):
    result = blake128_with_key(value, b"\x00" * 16)
    assert result.hex() == "b98324686a2c8327451b02f3a280c0f2"


@pytest.mark.parametrize("value", ["deadbeef"])
def test_blake160(value):
    result = blake160(value)
    assert result.hex() == "e8c8d008ee369e385cff36246425c7b30696a2b1"


@pytest.mark.parametrize("value", ["deadbeef"])
def test_blake160_with_key(value):
    result = blake160_with_key(value, b"\x00" * 16)
    assert result.hex() == "850b2b598a7782fe904860fbec66d396697fa47b"


@pytest.mark.parametrize("value", ["deadbeef"])
def test_blake256(value):
    result = blake256(value)
    assert (
        result.hex()
        == "f3e925002fed7cc0ded46842569eb5c90c910c091d8d04a1bdf96e0db719fd91"
    )


@pytest.mark.parametrize("value", ["deadbeef"])
def test_blake256_with_key(value):
    result = blake256_with_key(value, b"\x00" * 16)
    assert (
        result.hex()
        == "f247b4a8963b51a380cd5065a62c5b847fc84de899c41cd9d9dd0133d8980602"
    )


@pytest.mark.parametrize("value", ["deadbeef"])
def test_ripemd160(value):
    result = ripemd160(value)
    assert result.hex() == "226821c2f5423e11fe9af68bd285c249db2e4b5a"
