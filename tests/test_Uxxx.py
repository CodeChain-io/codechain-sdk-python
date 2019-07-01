from context import codechain_primitives
from codechain_primitives import U64, U128, U256
import pytest
import inspect
from rlp import encode, decode
from rlp.sedes import big_endian_int

TOO_LARGE = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_unsigned_integer(Uxxx, className, byteLength):
    def test_import():
        assert inspect.isclass(Uxxx)


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_new(Uxxx, className, byteLength):
    assert Uxxx(16).eq(Uxxx("16"))
    assert Uxxx(16).eq(Uxxx("0x10"))
    with pytest.raises(ValueError):
        assert Uxxx(TOO_LARGE)

    assert Uxxx(Uxxx(16)).eq(Uxxx(16))
    if type(Uxxx) is U256:
        assert Uxxx(16).eq(U256(U64(16)))
        assert Uxxx(16).eq(U256(U128(16)))
    elif type(Uxxx) is U128:
        assert Uxxx(16).eq(U128(U64(16)))


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_check(Uxxx, className, byteLength):
    assert Uxxx.check(-1) == False
    assert Uxxx.check(0.5) == False

    assert Uxxx.check(0) == True
    assert Uxxx.check("0") == True
    assert Uxxx.check("0x0") == True

    if byteLength >= 32:
        assert Uxxx.check(U256(0)) == True
    if byteLength >= 16:
        assert Uxxx.check(U128(0)) == True
    assert Uxxx.check(U64(0)) == True


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_ensure(Uxxx, className, byteLength):
    assert Uxxx("10").eq(Uxxx(10))
    assert Uxxx("0xa").eq(Uxxx(10))
    assert Uxxx(Uxxx(10)).eq(Uxxx(10))

    if byteLength >= 32:
        assert Uxxx(U256(10)).eq(Uxxx(10))
    if byteLength >= 16:
        assert Uxxx(U128(10)).eq(Uxxx(10))
    assert Uxxx(U64(10)).eq(Uxxx(10))


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_from_rlp(Uxxx, className, byteLength):
    value = Uxxx(0)
    assert Uxxx.from_rlp(value.rlp_bytes()).eq(value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value
    value = Uxxx(1)
    assert Uxxx.from_rlp(value.rlp_bytes()).eq(value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value
    value = Uxxx(0x79)
    assert Uxxx.from_rlp(value.rlp_bytes()).eq(value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value
    value = Uxxx(255)
    assert Uxxx.from_rlp(value.rlp_bytes()).eq(value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value
    value = Uxxx(1000)
    assert Uxxx.from_rlp(value.rlp_bytes()).eq(value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value
    value = Uxxx("1000000000000000")
    assert Uxxx.from_rlp(value.rlp_bytes()).eq(value)
    assert Uxxx(decode(value.rlp_bytes(), big_endian_int)) == value

    rlpdata = [0x80 + byteLength] + [0xff for i in range(byteLength)]
    assert Uxxx.from_rlp(bytes(rlpdata)).eq(Uxxx.MAX_VALUE())


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_from_rlp_throws_for_oversize_buffer(Uxxx, className, byteLength):
    with pytest.raises(ValueError) as e:
        rlpdata = chr(0x80 + byteLength + 1).ljust(byteLength + 2, chr(0xff))
        Uxxx.from_rlp(rlpdata).eq(Uxxx.MAX_VALUE())
    assert "less than or equal to" in str(e.value)


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_from_rlp_throws_for_invalid_RLP(Uxxx, className, byteLength):
    with pytest.raises(ValueError) as e:
        rlpdata = chr(0xc0 + byteLength + 1).ljust(byteLength + 1, chr(0xff))
        Uxxx.from_rlp(rlpdata).eq(Uxxx.MAX_VALUE())
    assert "Invalid data" in str(e.value)


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_is_equal_to(Uxxx, className, byteLength):
    assert Uxxx(0).is_equal_to(Uxxx(0))
    assert Uxxx(1000000).is_equal_to(Uxxx(1000000))
    assert Uxxx("100000000000000000").is_equal_to(Uxxx("100000000000000000"))


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_rlp_bytes(Uxxx, className, byteLength):
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


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_to_encode_object(Uxxx, className, byteLength):
    assert Uxxx(0).to_encode_object() == b"\x00"
    assert Uxxx(0xf).to_encode_object() == b"\x0f"
    assert Uxxx(0xff).to_encode_object() == b"\xff"
    assert Uxxx(0xfff).to_encode_object() == b"\x0f\xff"


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_to_string(Uxxx, className, byteLength):
    assert Uxxx(0).to_string() == "0x0"
    assert Uxxx(0).to_string(10) == "0"
    assert Uxxx(0).to_string(16) == "0x0"
    assert Uxxx(0).to_string(16, False) == "0"
    assert Uxxx(0xff).to_string(10) == "255"
    assert Uxxx(0xff).to_string(16) == "0xff"

    assert str(Uxxx(0)) == "0"
    assert str(Uxxx(0xff)) == "255"


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_to_json(Uxxx, className, byteLength):
    assert Uxxx(0).to_json() == "0x0"
    assert Uxxx(0xff).to_json() == "0xff"


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_from_json(Uxxx, className, byteLength):
    assert Uxxx.from_json("0x0") == Uxxx(0x0)
    assert Uxxx.from_json("0xff") == Uxxx(0xff)


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_plus(Uxxx, className, byteLength):
    assert Uxxx(10) + Uxxx(5) == Uxxx(10 + 5)
    with pytest.raises(ValueError) as e:
        Uxxx(Uxxx.MAX_VALUE) + Uxxx(1)
    assert "overflow" in str(e.value)
    with pytest.raises(ValueError) as e:
        Uxxx(-1) + Uxxx(0)
    assert "Invalid" in str(e.value)

    a = Uxxx(10)
    b = Uxxx(5)
    assert (a + b) == Uxxx(15)
    c = Uxxx(Uxxx.MAX_VALUE())
    d = Uxxx(1)
    with pytest.raises(ValueError) as e:
        (c + d)
    assert "overflow" in str(e.value)


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_minus(Uxxx, className, byteLength):
    assert Uxxx(10) - Uxxx(5) == Uxxx(10 - 5)
    with pytest.raises(ValueError) as e:
        Uxxx(5) - Uxxx(10)
    assert "underflow" in str(e.value)
    with pytest.raises(ValueError) as e:
        Uxxx(-1) - Uxxx(-1)
    assert "Invalid" in str(e.value)

    a = Uxxx(10)
    b = Uxxx(5)
    assert (a - b) == Uxxx(10 - 5)
    with pytest.raises(ValueError) as e:
        b - a
    assert "underflow" in str(e.value)


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_times(Uxxx, className, byteLength):
    assert Uxxx(10) * Uxxx(5) == Uxxx(10 * 5)
    assert Uxxx(Uxxx.MAX_VALUE) * Uxxx(0) == Uxxx(0)
    assert Uxxx(Uxxx.MAX_VALUE) * Uxxx(1) == Uxxx.MAX_VALUE()
    with pytest.raises(ValueError) as e:
        Uxxx(Uxxx.MAX_VALUE) * Uxxx(2)
    assert "overflow" in str(e.value)
    with pytest.raises(ValueError) as e:
        Uxxx(-1) * Uxxx(-1)
    assert "Invalid" in str(e.value)

    a = Uxxx(10)
    b = Uxxx(5)
    assert (a * b) == Uxxx(10 * 5)
    c = Uxxx.MAX_VALUE()
    d = Uxxx(0)
    assert (c * d) == Uxxx(0)
    e = Uxxx(1)
    assert (c * e) == (c)
    f = Uxxx(2)
    with pytest.raises(ValueError) as e:
        c * f
    assert "overflow" in str(e.value)


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_idiv(Uxxx, className, byteLength):
    assert Uxxx(10) // Uxxx(5) == Uxxx(10 // 5)
    assert Uxxx(14) // Uxxx(5) == Uxxx(2)
    with pytest.raises(ValueError) as e:
        Uxxx(10) // Uxxx(0)
    assert "Divided" in str(e.value)
    Uxxx(-1) // Uxxx(-1) == Uxxx(1)

    a = Uxxx(10)
    b = Uxxx(5)
    assert (a // b) == Uxxx(10//5)
    c = Uxxx(14)
    assert (c // b) == Uxxx(2)
    d = Uxxx(0)
    with pytest.raises(ValueError) as e:
        (a // d)
    assert "Divided" in str(e.value)


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_mod(Uxxx, className, byteLength):
    assert Uxxx(10) % Uxxx(5) == Uxxx(0)
    assert Uxxx(14) % Uxxx(5) == Uxxx(4)
    with pytest.raises(ValueError) as e:
        Uxxx(10) % Uxxx(0)
    assert "Divided" in str(e.value)
    with pytest.raises(ValueError) as e:
        Uxxx(-1) % Uxxx(-1)
    assert "Invalid" in str(e.value)

    a = Uxxx(10)
    b = Uxxx(5)
    assert (a % b) == Uxxx(0)
    c = Uxxx(14)
    assert (c % b) == Uxxx(4)
    d = Uxxx(0)
    with pytest.raises(ValueError) as e:
        a % d
    assert "Divided" in str(e.value)


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_comparison(Uxxx, className, byteLength):
    assert Uxxx(11) > (10) == True
    assert Uxxx(10) > (10) == False
    assert Uxxx(9) > (10) == False

    assert Uxxx(11) >= (10) == True
    assert Uxxx(10) >= (10) == True
    assert Uxxx(9) >= (10) == False

    assert Uxxx(11) < (10) == False
    assert Uxxx(10) < (10) == False
    assert Uxxx(9) < (10) == True

    assert Uxxx(11) <= (10) == False
    assert Uxxx(10) <= (10) == True
    assert Uxxx(9) <= (10) == True


@pytest.mark.parametrize("Uxxx, className, byteLength", [(U64, "U64", 8), (U128, "U128", 16), (U256, "U256", 32)])
def test_comparison(Uxxx, className, byteLength):
    assert Uxxx(1234567).to_locale_string() == "1,234,567"
    assert Uxxx(123).to_locale_string() == "123"
