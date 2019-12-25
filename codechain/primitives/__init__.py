import sys

from .assetaddress import AssetAddress
from .assetaddress import MultiSig
from .hexstring import H128
from .hexstring import H160
from .hexstring import H256
from .hexstring import H512
from .platformaddress import PlatformAddress
from .unsignedinteger import U128
from .unsignedinteger import U256
from .unsignedinteger import U64

# -------
# Pythons
# -------

if sys.version_info < (3, 6):
    raise ValueError("Please use >=python3.6")
