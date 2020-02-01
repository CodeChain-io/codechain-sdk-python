#!/usr/bin/python3
from codechain.keystore import CCkey

keystore = CCkey.create()
key = keystore.platform.create_key()

print(key)
