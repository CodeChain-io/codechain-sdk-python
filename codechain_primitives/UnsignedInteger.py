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

    def __add__(self, rhs_value):
        return self.__class__(int(self) + int(rhs_value))

    def __radd__(self, lhs_value):
        return self.__class__(int(lhs_value) + int(self))

    def __sub__(self, rhs_value):
        return self.__class__(int(self) - int(rhs_value))

    def __rsub__(self, lhs_value):
        return self.__class__(int(lhs_value) - int(self))

    def __mul__(self, rhs_value):
        return self.__class__(int(self) * int(rhs_value))

    def __rmul__(self, lhs_value):
        return self.__class__(int(lhs_value) * int(self))

    def __floordiv__(self, rhs_value):
        return self.__class__(int(self) // int(rhs_value))

    def __rfloordiv__(self, lhs_value):
        return self.__class__(int(lhs_value) // int(self))

    def __mod__(self, rhs_value):
        return self.__class__(int(self) % int(rhs_value))

    def __rmod__(self, lhs_value):
        return self.__class__(int(lhs_value) % int(self))

    @classmethod
    def from_rlp(cls, buffer):
        if not isinstance(buffer, (bytes, bytearray)):
            raise ValueError("Argument should be bytearray")
        data = buffer[1:]
        first = buffer[0]
        if first < 0x80:
            return cls(hex(first))

        length = first - 0x80
        max_bytes = (cls.MAX_VALUE.bit_length() + 7) // 8
        if len(data) != length:
            raise ValueError("Invalid data for Unsigned integer")
        elif length > max_bytes:
            raise ValueError(f"Byte length of {cls.__name__} must be less than or equal to {max_bytes}")
        elif length == 0:
            return cls('0')
        return cls(int.from_bytes(data, byteorder='big'))

    @classmethod
    def check_string(cls, param):
        if not isinstance(param, str):
            return False
        try:
            value = int(param, 0)
            return value >= 0 and value <= cls.MAX_VALUE
        except:
            return False

    @classmethod
    def check(cls, param):
        if isinstance(param, str):
            return cls.check_string(param)
        else:
            if not isinstance(param, int):
                return False
        if param >= 0 and param <= cls.MAX_VALUE:
            return True
        return False

    def to_encode_object(self):
        return self

    def rlp_bytes(self):
        return encode(self.to_encode_object())

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
