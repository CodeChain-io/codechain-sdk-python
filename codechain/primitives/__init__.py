import sys

from .HexString import H128
from .HexString import H160
from .HexString import H256
from .HexString import H512
from .UnsignedInteger import U128
from .UnsignedInteger import U256
from .UnsignedInteger import U64

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = _ver[0] == 2

#: Python 3.x?
is_py3 = _ver[0] == 3

if is_py2:
    raise ValueError("Please use python3")
