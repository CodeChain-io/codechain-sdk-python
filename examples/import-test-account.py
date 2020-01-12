#!/usr/bin/python3
from codechain import SDK

sdk = SDK("http://localhost:8080", "tc")

ACCOUNT_SECRET = "ede1d4ccb4ec9a8bbbae9a13db3f4a7b56ea04189be86ac3a6a439d9a0a1addd"
ACCOUNT_PASSPHRASE = "satoshi"


address = sdk.rpc.account.import_raw(ACCOUNT_SECRET, ACCOUNT_PASSPHRASE)

print(address)
