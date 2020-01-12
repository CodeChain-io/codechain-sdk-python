#!/usr/bin/python3
from codechain import SDK

sdk = SDK("http://localhost:8080", "tc")

ACCOUNT_ADDRESS = "tccq9h7vnl68frvqapzv3tujrxtxtwqdnxw6yamrrgd"
ACCOUNT_PASSPHRASE = "satoshi"

address = "tcaqyqckq0zgdxgpck6tjdg4qmp52p2vx3qaexqnegylk"

tx = sdk.core.create_mint_asset_transaction(
    address,
    None,
    None,
    None,
    0,
    {"name": "Silver Coin", "description": "...", "icon_url": "..."},
    None,
    None,
    None,
    100000000,
)

tx_hash = sdk.rpc.chain.send_transaction(tx, ACCOUNT_ADDRESS, ACCOUNT_PASSPHRASE)

result = sdk.rpc.chain.contains_transaction(tx_hash)

print(result)
