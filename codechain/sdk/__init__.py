import sys

from .sdk import SDK

# -------
# Pythons
# -------

if sys.version_info < (3, 6):
    raise ValueError("Please use >=python3.6")
