from .UnsignedInteger import U64, U128, U256
from .HexString import H128, H160, H256, H512

import sys
# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

if is_py2:
    raise ValueError("Please use python3")
