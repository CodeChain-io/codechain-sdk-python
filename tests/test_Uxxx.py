import inspect

import pytest
from context import codechain
from rlp import decode
from rlp import encode
from rlp.sedes import big_endian_int

from codechain.primitives import U128
from codechain.primitives import U256
from codechain.primitives import U64

TOO_LARGE = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_import(Uxxx, byteLength):
    assert inspect.isclass(Uxxx)


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_new(Uxxx, byteLength):
    assert Uxxx(16) == (Uxxx("16"))
    assert Uxxx(16) == (Uxxx("0x10"))
    with pytest.raises(ValueError):
        assert Uxxx(TOO_LARGE)

    assert Uxxx(Uxxx(16)) == (Uxxx(16))
    if type(Uxxx) is U256:
        assert Uxxx(16) == (U256(U64(16)))
        assert Uxxx(16) == (U256(U128(16)))
    elif type(Uxxx) is U128:
        assert Uxxx(16) == (U128(U64(16)))


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_check(Uxxx, byteLength):
    assert Uxxx.check(-1) is False
    assert Uxxx.check(0.5) is False

    assert Uxxx.check(0) is True
    assert Uxxx.check("0") is True
    assert Uxxx.check("0x0") is True

    if byteLength >= 32:
        assert Uxxx.check(U256(0)) is True
    if byteLength >= 16:
        assert Uxxx.check(U128(0)) is True
    assert Uxxx.check(U64(0)) is True


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_ensure(Uxxx, byteLength):
    assert Uxxx("10") == Uxxx(10)
    assert Uxxx("0xa") == Uxxx(10)
    assert Uxxx(Uxxx(10))

    if byteLength >= 32:
        assert Uxxx(U256(10)) == (Uxxx(10))
    if byteLength >= 16:
        assert Uxxx(U128(10)) == (Uxxx(10))
    assert Uxxx(U64(10)) == (Uxxx(10))


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_from_rlp(Uxxx, byteLength):
    value = Uxxx(0)
    assert Uxxx.from_rlp(value.rlp_bytes()) == (value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value
    value = Uxxx(1)
    assert Uxxx.from_rlp(value.rlp_bytes()) == (value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value
    value = Uxxx(0x79)
    assert Uxxx.from_rlp(value.rlp_bytes()) == (value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value
    value = Uxxx(255)
    assert Uxxx.from_rlp(value.rlp_bytes()) == (value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value
    value = Uxxx(1000)
    assert Uxxx.from_rlp(value.rlp_bytes()) == (value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value
    value = Uxxx("1000000000000000")
    assert Uxxx.from_rlp(value.rlp_bytes()) == (value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value

    rlpdata = [0x80 + byteLength] + [0xFF for i in range(byteLength)]
    assert Uxxx.from_rlp(bytes(rlpdata)) == (Uxxx.MAX_VALUE)


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_from_rlp_throws_for_oversize_buffer(Uxxx, byteLength):
    with pytest.raises(ValueError) as e:
        rlpdata = [0x80 + byteLength + 1] + [0xFF for i in range(byteLength + 1)]
        assert Uxxx.from_rlp(bytes(rlpdata)) == (Uxxx.MAX_VALUE)
    assert "less than or equal to" in str(e.value)


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_from_rlp_throws_for_invalid_RLP(Uxxx, byteLength):
    with pytest.raises(ValueError) as e:
        rlpdata = [0x80 + byteLength + 1] + [0xFF for i in range(byteLength)]
        assert Uxxx.from_rlp(bytes(rlpdata)) == (Uxxx.MAX_VALUE)
    assert "Invalid data" in str(e.value)


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_is_equal_to(Uxxx, byteLength):
    assert Uxxx(0) == Uxxx(0)
    assert Uxxx(1000000) == Uxxx(1000000)
    assert Uxxx("100000000000000000") == Uxxx("100000000000000000")


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_rlp_bytes(Uxxx, byteLength):
    assert Uxxx(0).rlp_bytes() == b"\x80"
    assert Uxxx(10).rlp_bytes() == b"\x0a"
    assert Uxxx(255).rlp_bytes() == b"\x81\xff"
    assert Uxxx(1000).rlp_bytes() == b"\x82\x03\xe8"
    assert Uxxx(100000).rlp_bytes() == b"\x83\x01\x86\xa0"
    assert Uxxx(10000000).rlp_bytes() == b"\x83\x98\x96\x80"
    assert Uxxx("1000000000").rlp_bytes() == b"\x84\x3b\x9a\xca\x00"
    assert Uxxx("1000000000000").rlp_bytes() == b"\x85\xe8\xd4\xa5\x10\x00"

    assert encode(Uxxx(0)) == b"\x80"
    assert encode(Uxxx(10)) == b"\x0a"
    assert encode(Uxxx(255)) == b"\x81\xff"
    assert encode(Uxxx(1000)) == b"\x82\x03\xe8"
    assert encode(Uxxx(100000)) == b"\x83\x01\x86\xa0"
    assert encode(Uxxx(10000000)) == b"\x83\x98\x96\x80"
    assert encode(Uxxx("1000000000")) == b"\x84\x3b\x9a\xca\x00"
    assert encode(Uxxx("1000000000000")) == b"\x85\xe8\xd4\xa5\x10\x00"


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_to_encode_object(Uxxx, byteLength):
    assert Uxxx(0).to_encode_object() == 0
    assert Uxxx(0xF).to_encode_object() == 0xF
    assert Uxxx(0xFF).to_encode_object() == 0xFF
    assert Uxxx(0xFFF).to_encode_object() == 0xFFF


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_to_string(Uxxx, byteLength):
    assert Uxxx(0).to_string() == "0x0"
    assert Uxxx(0).to_string(10) == "0"
    assert Uxxx(0).to_string(16) == "0x0"
    assert Uxxx(0).to_string(16, False) == "0"
    assert Uxxx(0xFF).to_string(10) == "255"
    assert Uxxx(0xFF).to_string(16) == "0xff"

    assert str(Uxxx(0)) == "0"
    assert str(Uxxx(0xFF)) == "255"


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_to_json(Uxxx, byteLength):
    assert Uxxx(0).to_json() == "0x0"
    assert Uxxx(0xFF).to_json() == "0xff"


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_from_json(Uxxx, byteLength):
    assert Uxxx.from_json("0x0") == Uxxx(0x0)
    assert Uxxx.from_json("0xff") == Uxxx(0xFF)


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_plus(Uxxx, byteLength):
    assert Uxxx(10) + Uxxx(5) == Uxxx(10 + 5)
    with pytest.raises(ValueError) as e:
        Uxxx(Uxxx.MAX_VALUE) + Uxxx(1)
    assert "overflow" in str(e.value)
    with pytest.raises(ValueError) as e:
        Uxxx(0) - 1
    assert "underflow" in str(e.value)

    a = Uxxx(10)
    b = Uxxx(5)
    assert (a + b) == Uxxx(15)
    c = Uxxx(Uxxx.MAX_VALUE)
    d = Uxxx(1)
    with pytest.raises(ValueError) as e:
        (c + d)
    assert "overflow" in str(e.value)


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_minus(Uxxx, byteLength):
    assert Uxxx(10) - Uxxx(5) == Uxxx(10 - 5)
    with pytest.raises(ValueError) as e:
        Uxxx(5) - Uxxx(10)
    assert "underflow" in str(e.value)
    with pytest.raises(ValueError) as e:
        Uxxx(5) - 10
    assert "underflow" in str(e.value)

    a = Uxxx(10)
    b = Uxxx(5)
    assert (a - b) == Uxxx(10 - 5)
    with pytest.raises(ValueError) as e:
        b - a
    assert "underflow" in str(e.value)


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_times(Uxxx, byteLength):
    assert Uxxx(10) * Uxxx(5) == Uxxx(10 * 5)
    assert Uxxx(Uxxx.MAX_VALUE) * Uxxx(0) == Uxxx(0)
    assert Uxxx(Uxxx.MAX_VALUE) * Uxxx(1) == Uxxx.MAX_VALUE
    with pytest.raises(ValueError) as e:
        Uxxx(Uxxx.MAX_VALUE) * Uxxx(2)
    assert "overflow" in str(e.value)
    with pytest.raises(ValueError) as e:
        Uxxx(-1) * Uxxx(-1)
    assert "underflow" in str(e.value)

    a = Uxxx(10)
    b = Uxxx(5)
    assert (a * b) == Uxxx(10 * 5)
    c = Uxxx.MAX_VALUE
    d = Uxxx(0)
    assert (c * d) == Uxxx(0)
    e = Uxxx(1)
    assert (c * e) == (c)
    f = Uxxx(2)
    with pytest.raises(ValueError) as e:
        c * f
    assert "overflow" in str(e.value)


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_idiv(Uxxx, byteLength):
    assert Uxxx(10) // Uxxx(5) == Uxxx(10 // 5)
    assert Uxxx(14) // Uxxx(5) == Uxxx(2)
    with pytest.raises(ZeroDivisionError) as e:
        Uxxx(10) // Uxxx(0)
    assert "division" in str(e.value)
    with pytest.raises(ValueError) as e:
        Uxxx(1) // -1
    assert "underflow" in str(e.value)

    a = Uxxx(10)
    b = Uxxx(5)
    assert (a // b) == Uxxx(10 // 5)
    c = Uxxx(14)
    assert (c // b) == Uxxx(2)
    d = Uxxx(0)
    with pytest.raises(ZeroDivisionError) as e:
        (a // d)
    assert "division" in str(e.value)


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_mod(Uxxx, byteLength):
    assert Uxxx(10) % Uxxx(5) == Uxxx(0)
    assert Uxxx(14) % Uxxx(5) == Uxxx(4)
    with pytest.raises(ZeroDivisionError) as e:
        Uxxx(10) % Uxxx(0)
    assert "modulo" in str(e.value)
    assert Uxxx(1) % -1 == 0

    a = Uxxx(10)
    b = Uxxx(5)
    assert (a % b) == Uxxx(0)
    c = Uxxx(14)
    assert (c % b) == Uxxx(4)
    d = Uxxx(0)
    with pytest.raises(ZeroDivisionError) as e:
        a % d
    assert "modulo" in str(e.value)


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_comparison(Uxxx, byteLength):
    assert (Uxxx(11) > (10)) is True
    assert (Uxxx(10) > (10)) is False
    assert (Uxxx(9) > (10)) is False

    assert (Uxxx(11) >= (10)) is True
    assert (Uxxx(10) >= (10)) is True
    assert (Uxxx(9) >= (10)) is False

    assert (Uxxx(11) < (10)) is False
    assert (Uxxx(10) < (10)) is False
    assert (Uxxx(9) < (10)) is True

    assert (Uxxx(11) <= (10)) is False
    assert (Uxxx(10) <= (10)) is True
    assert (Uxxx(9) <= (10)) is True


@pytest.mark.parametrize("Uxxx, byteLength", [(U64, 8), (U128, 16), (U256, 32)])
def test_to_locale_string(Uxxx, byteLength):
    assert Uxxx(1234567).to_locale_string() == "1,234,567"
    assert Uxxx(123).to_locale_string() == "123"
