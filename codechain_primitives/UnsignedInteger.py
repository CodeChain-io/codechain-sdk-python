from rlp import encode


class _UnsignedInteger(int):
    """UnsignedInteger base class: all unsigned integer inherit from this class.
    """

    def __new__(cls, *args, **kwargs):
        assert(hasattr(cls, "MAX_VALUE"), f"{cls.__name__} should have a class variable 'MAX_VALUE'")

        if isinstance(args[0], str):
            result = super().__new__(cls, *args, **kwargs, base=0)
        else:
            result = super().__new__(cls, *args, **kwargs)

        if result < 0:
            raise ValueError("Integer underflow")
        if hasattr(cls, 'MAX_VALUE') and result > cls.MAX_VALUE:
            raise ValueError("Integer overflow")
        return result

    def __add__(self, rhsValue):
        return self.__class__(int(self) + int(rhsValue))

    def __radd__(self, lhsValue):
        return self.__class__(int(lhsValue) + int(self))

    def __sub__(self, rhsValue):
        return self.__class__(int(self) - int(rhsValue))

    def __rsub__(self, lhsValue):
        return self.__class__(int(lhsValue) - int(self))

    def __mul__(self, rhsValue):
        return self.__class__(int(self) * int(rhsValue))

    def __rmul__(self, lhsValue):
        return self.__class__(int(lhsValue) * int(self))

    def __floordiv__(self, rhsValue):
        return self.__class__(int(self) // int(rhsValue))

    def __rfloordiv__(self, lhsValue):
        return self.__class__(int(lhsValue) // int(self))

    def __mod__(self, rhsValue):
        return self.__class__(int(self) % int(rhsValue))

    def __rmod__(self, lhsValue):
        return self.__class__(int(lhsValue) % int(self))

    @classmethod
    def from_rlp(cls, buffer):
        if type(buffer) is not bytes and type(buffer) is not bytearray:
            raise ValueError("Argument should be bytearray")
        data = buffer[1:]
        first = buffer[0]
        if first < 0x80:
            return cls(hex(first))

        length = first - 0x80
        if len(data) != length:
            raise ValueError("Invalid data for Unsigned integer")
        elif length > len(bytes.fromhex(hex(cls.MAX_VALUE)[2:])):
            raise ValueError(
                f"Data for Unsigned integer must be less than or equal to {len(bytes.fromhex(hex(cls.MAX_VALUE)[2:]))}")
        elif length == 0:
            return cls('0')
        return cls(int.from_bytes(data, byteorder='big'))

    @classmethod
    def check_string(cls, param):
        if type(param) is not str:
            return False
        try:
            value = int(param, 0)
            return value >= 0 and value <= cls.MAX_VALUE
        except:
            return False

    @classmethod
    def check(cls, param):
        if type(param) is str:
            return cls.check_string(param)
        else:
            if not isinstance(param, int):
                return False
        if param >= 0 and param <= cls.MAX_VALUE:
            return True
        return False

    def to_encode_object(self):
        result = hex(int(self))[2:]
        result = "0" + result if len(result) % 2 == 1 else result
        return bytes.fromhex(result)

    def rlp_bytes(self):
        return encode(self)

    def to_string(self, base=16, prefix=True):
        if base == 10:
            return str(self)
        elif base == 16 and prefix:
            return hex(self)
        elif base == 16 and not prefix:
            return "{:x}".format(self)
        else:
            raise ValueError("Only supports base 10, 16")

    def to_locale_string(self):
        return "{:,}".format(self)

    def to_json(self):
        return hex(int(self))

    @classmethod
    def from_json(cls, string):
        return cls(string)


class U64(_UnsignedInteger):
    MAX_VALUE = 0xFFFFFFFFFFFFFFFF


class U128(_UnsignedInteger):
    MAX_VALUE = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


class U256(_UnsignedInteger):
    MAX_VALUE = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
