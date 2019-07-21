import inspect

import pytest
from context import codechain
from rlp import decode
from rlp import encode

from codechain.primitives import H128
from codechain.primitives import H160
from codechain.primitives import H256
from codechain.primitives import H512


@pytest.mark.parametrize(
    "Hxxx, className, byteLength",
    [(H128, "H128", 16), (H160, "H160", 20), (H256, "H256", 32), (H512, "H512", 64)],
)
def test_import(Hxxx, className, byteLength):
    assert inspect.isclass(Hxxx)


@pytest.mark.parametrize(
    "Hxxx, className, byteLength",
    [(H128, "H128", 16), (H160, "H160", 20), (H256, "H256", 32), (H512, "H512", 64)],
)
def test_new(Hxxx, className, byteLength):
    zero = "00" * byteLength
    Hxxx(zero)
    Hxxx(f"0x{zero}")
    with pytest.raises(ValueError) as e:
        Hxxx(zero + "0")
    assert str(byteLength) in str(e.value)
    with pytest.raises(ValueError) as e:
        Hxxx(zero[1:])
    assert str(byteLength) in str(e.value)


@pytest.mark.parametrize(
    "Hxxx, className, byteLength",
    [(H128, "H128", 16), (H160, "H160", 20), (H256, "H256", 32), (H512, "H512", 64)],
)
def test_zero(Hxxx, className, byteLength):
    zero = "00" * byteLength
    assert Hxxx(zero) == Hxxx(Hxxx.ZERO)


@pytest.mark.parametrize(
    "Hxxx, className, byteLength",
    [(H128, "H128", 16), (H160, "H160", 20), (H256, "H256", 32), (H512, "H512", 64)],
)
def test_check(Hxxx, className, byteLength):
    zero = "00" * byteLength
    assert Hxxx.check(Hxxx(zero)) == True
    assert Hxxx.check(zero) == True
    assert Hxxx.check(zero[1:] + "F") == True
    assert Hxxx.check(zero[1:] + "f") == True
    assert Hxxx.check(zero[1:] + "G") == False
    assert Hxxx.check(zero[1:] + "g") == False
    assert Hxxx.check(zero + "0") == False


@pytest.mark.parametrize(
    "Hxxx, className, byteLength",
    [(H128, "H128", 16), (H160, "H160", 20), (H256, "H256", 32), (H512, "H512", 64)],
)
def test_ensure(Hxxx, className, byteLength):
    zero = "00" * byteLength
    assert Hxxx(Hxxx(zero)) == Hxxx(zero)


@pytest.mark.parametrize(
    "Hxxx, className, byteLength",
    [(H128, "H128", 16), (H160, "H160", 20), (H256, "H256", 32), (H512, "H512", 64)],
)
def test_from_rlp_zero(Hxxx, className, byteLength):
    zero = "00" * byteLength
    zeroBytes = []
    if byteLength <= 55:
        zeroBytes = [0x80 + byteLength] + [0 for i in range(byteLength)]
    elif byteLength <= 0xFF:
        zeroBytes = [0xB8, byteLength] + [0 for i in range(byteLength)]
    else:
        raise ValueError("Not implemented")
    assert Hxxx.from_rlp(bytes(zeroBytes)) == Hxxx(zero)
    assert Hxxx(decode(bytes(zeroBytes))) == Hxxx(zero)


@pytest.mark.parametrize(
    "Hxxx, className, byteLength",
    [(H128, "H128", 16), (H160, "H160", 20), (H256, "H256", 32), (H512, "H512", 64)],
)
def test_from_rlp_FF(Hxxx, className, byteLength):
    value = "FF" * byteLength
    valueBytes = []
    if byteLength <= 55:
        valueBytes = [0x80 + byteLength] + [0xFF for i in range(byteLength)]
    elif byteLength <= 0xFF:
        valueBytes = [0xB8, byteLength] + [0xFF for i in range(byteLength)]
    else:
        raise ValueError("Not implemented")

    assert Hxxx.from_rlp(bytes(valueBytes)) == Hxxx(value)


@pytest.mark.parametrize(
    "Hxxx, className, byteLength",
    [(H128, "H128", 16), (H160, "H160", 20), (H256, "H256", 32), (H512, "H512", 64)],
)
def test_from_rlp_throws(Hxxx, className, byteLength):
    longerZeroBytes = []
    if byteLength <= 55:
        longerZeroBytes = [0x80 + byteLength + 1] + [0 for i in range(byteLength + 1)]
    elif byteLength <= 0xFF:
        longerZeroBytes = [0xB8, byteLength + 1] + [0 for i in range(byteLength + 1)]
    else:
        raise ValueError("Not implemented")
    with pytest.raises(ValueError) as e:
        Hxxx.from_rlp(bytes(longerZeroBytes))
    assert "Expected" in str(e.value)

    with pytest.raises(ValueError) as e:
        Hxxx.from_rlp(longerZeroBytes)
    assert "Argument should be bytearray" in str(e.value)


@pytest.mark.parametrize(
    "Hxxx, className, byteLength",
    [(H128, "H128", 16), (H160, "H160", 20), (H256, "H256", 32), (H512, "H512", 64)],
)
def test_is_equal_to(Hxxx, className, byteLength):
    zero = "00" * byteLength
    one = "00" * (byteLength - 1) + "01"

    assert Hxxx(zero) == Hxxx(zero)
    assert Hxxx(zero) != Hxxx(one)


@pytest.mark.parametrize(
    "Hxxx, className, byteLength",
    [(H128, "H128", 16), (H160, "H160", 20), (H256, "H256", 32), (H512, "H512", 64)],
)
def test_rlp_bytes(Hxxx, className, byteLength):
    zero = "00" * byteLength
    if byteLength <= 55:
        result = bytearray()
        result.extend(map(ord, (chr(0x80 + byteLength) + "\x00" * byteLength)))
        assert Hxxx(zero).rlp_bytes() == result
        assert encode(Hxxx(zero)) == result
    elif byteLength <= 0xFF:
        result = bytearray()
        result.extend(map(ord, (chr(0xB8) + chr(byteLength) + "\x00" * byteLength)))
        assert Hxxx(zero).rlp_bytes() == result
        assert encode(Hxxx(zero)) == result
    else:
        raise ValueError("Not implemented")
