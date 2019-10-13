import sys

from .Pbkdf2 import pbkdf2

# -------
# Pythons
# -------

if sys.version_info < (3, 6):
    raise ValueError("Please use >=python3.6")
