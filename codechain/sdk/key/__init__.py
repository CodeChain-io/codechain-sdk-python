import sys

from .key import Key
from .key import KeyStoreType

# -------
# Pythons
# -------

if sys.version_info < (3, 6):
    raise ValueError("Please use >=python3.6")
