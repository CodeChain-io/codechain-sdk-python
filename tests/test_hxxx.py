import inspect

import pytest
from context import codechain
from rlp import decode
from rlp import encode

from codechain.primitives import H128
from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import H512


@pytest.mark.parametrize("Hxxx", [H128, H160, H256, H512])
def test_import(Hxxx):
    assert inspect.isclass(Hxxx)


@pytest.mark.parametrize(
    "Hxxx, byte_length", [(H128, 16), (H160, 20), (H256, 32), (H512, 64)]
)
def test_new(Hxxx, byte_length):
    zero = "00" * byte_length
    Hxxx(zero)
    Hxxx(f"0x{zero}")
    with pytest.raises(ValueError) as e:
        Hxxx(zero + "0")
    assert str(byte_length) in str(e.value)
    with pytest.raises(ValueError) as e:
        Hxxx(zero[1:])
    assert str(byte_length) in str(e.value)


@pytest.mark.parametrize(
    "Hxxx, byte_length", [(H128, 16), (H160, 20), (H256, 32), (H512, 64)]
)
def test_zero(Hxxx, byte_length):
    zero = "00" * byte_length
    assert Hxxx(zero) == Hxxx(Hxxx.ZERO)


@pytest.mark.parametrize(
    "Hxxx, byte_length", [(H128, 16), (H160, 20), (H256, 32), (H512, 64)]
)
def test_check(Hxxx, byte_length):
    zero = "00" * byte_length
    assert Hxxx.check(Hxxx(zero))
    assert Hxxx.check(zero)
    assert Hxxx.check(zero[1:] + "F")
    assert Hxxx.check(zero[1:] + "f")
    assert not Hxxx.check(zero[1:] + "G")
    assert not Hxxx.check(zero[1:] + "g")
    assert not Hxxx.check(zero + "0")


@pytest.mark.parametrize(
    "Hxxx, byte_length", [(H128, 16), (H160, 20), (H256, 32), (H512, 64)]
)
def test_ensure(Hxxx, byte_length):
    zero = "00" * byte_length
    assert Hxxx(Hxxx(zero)) == Hxxx(zero)


@pytest.mark.parametrize(
    "Hxxx, byte_length", [(H128, 16), (H160, 20), (H256, 32), (H512, 64)]
)
def test_from_rlp_zero(Hxxx, byte_length):
    zero = "00" * byte_length
    zero_bytes = []
    if byte_length <= 55:
        zero_bytes = [0x80 + byte_length] + [0 for i in range(byte_length)]
    elif byte_length <= 0xFF:
        zero_bytes = [0xB8, byte_length] + [0 for i in range(byte_length)]
    else:
        raise ValueError("Not implemented")
    assert Hxxx.from_rlp(bytes(zero_bytes)) == Hxxx(zero)
    assert Hxxx(decode(bytes(zero_bytes))) == Hxxx(zero)


@pytest.mark.parametrize(
    "Hxxx, byte_length", [(H128, 16), (H160, 20), (H256, 32), (H512, 64)]
)
def test_from_rlp_FF(Hxxx, byte_length):
    value = "FF" * byte_length
    value_bytes = []
    if byte_length <= 55:
        value_bytes = [0x80 + byte_length] + [0xFF for i in range(byte_length)]
    elif byte_length <= 0xFF:
        value_bytes = [0xB8, byte_length] + [0xFF for i in range(byte_length)]
    else:
        raise ValueError("Not implemented")

    assert Hxxx.from_rlp(bytes(value_bytes)) == Hxxx(value)


@pytest.mark.parametrize(
    "Hxxx, byte_length", [(H128, 16), (H160, 20), (H256, 32), (H512, 64)]
)
def test_from_rlp_throws(Hxxx, byte_length):
    longer_zero_bytes = []
    if byte_length <= 55:
        longer_zero_bytes = [0x80 + byte_length + 1] + [
            0 for i in range(byte_length + 1)
        ]
    elif byte_length <= 0xFF:
        longer_zero_bytes = [0xB8, byte_length + 1] + [
            0 for i in range(byte_length + 1)
        ]
    else:
        raise ValueError("Not implemented")
    with pytest.raises(ValueError) as e:
        Hxxx.from_rlp(bytes(longer_zero_bytes))
    assert "Expected" in str(e.value)

    with pytest.raises(ValueError) as e:
        Hxxx.from_rlp(longer_zero_bytes)
    assert "Argument should be bytearray" in str(e.value)


@pytest.mark.parametrize(
    "Hxxx, byte_length", [(H128, 16), (H160, 20), (H256, 32), (H512, 64)]
)
def test_is_equal_to(Hxxx, byte_length):
    zero = "00" * byte_length
    one = "00" * (byte_length - 1) + "01"

    assert Hxxx(zero) == Hxxx(zero)
    assert Hxxx(zero) != Hxxx(one)


@pytest.mark.parametrize(
    "Hxxx, byte_length", [(H128, 16), (H160, 20), (H256, 32), (H512, 64)]
)
def test_rlp_bytes(Hxxx, byte_length):
    zero = "00" * byte_length
    if byte_length <= 55:
        result = bytearray()
        result.extend(map(ord, (chr(0x80 + byte_length) + "\x00" * byte_length)))
        assert Hxxx(zero).rlp_bytes() == result
        assert encode(Hxxx(zero)) == result
    elif byte_length <= 0xFF:
        result = bytearray()
        result.extend(map(ord, (chr(0xB8) + chr(byte_length) + "\x00" * byte_length)))
        assert Hxxx(zero).rlp_bytes() == result
        assert encode(Hxxx(zero)) == result
    else:
        raise ValueError("Not implemented")


@pytest.mark.parametrize(
    "Hxxx, byte_length", [(H128, 16), (H160, 20), (H256, 32), (H512, 64)]
)
def test_to_json_and_to_stirng(Hxxx, byte_length):
    zero = "00" * byte_length
    hex_value = Hxxx(zero)

    assert hex_value.to_json() == zero


@pytest.mark.parametrize(
    "Hxxx, byte_length", [(H128, 16), (H160, 20), (H256, 32), (H512, 64)]
)
def test_to_string(Hxxx, byte_length):
    zero = "00" * byte_length
    hex_value = Hxxx(zero)

    assert str(hex_value) == zero
    assert hex_value.to_string() == zero
    assert hex_value.to_string(True) == "0x" + zero
