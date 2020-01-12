# CodeChain SDK for Python

A Python SDK for CodeChain.

## API Documentation (For SDK users)

Not prepared

## Getting Started (For SDK developers)

### Submitting patches
- Use `Black` to autoformat your code. This should be done for you as a git `pre-commit` hook.

### First time setup
- Clone your GitHub fork locally:
- Add the main repository as a remote to update later:
- Create a virtualenv using pipenv:
```shell
$ make init
```
- Install the pre-commit hooks:
```shell
$ pre-commit install --install-hooks
```
### Add dependency
- Install the dependency using pipenv
1. In the test environment
```shell
$ pipenv install [package] --dev
```
2. In the production
```shell
$ pip3 install [package]
```
and specify it to the `setup.py`
- lock the dependency
```shell
$ pipenv lock
```
### Run test cases
```shell
$ make test
```

## Usage

```python
#!/usr/bin/python3
from codechain import SDK

sdk = SDK("http://localhost:8080", "tc")

ACCOUNT_SECRET = "ede1d4ccb4ec9a8bbbae9a13db3f4a7b56ea04189be86ac3a6a439d9a0a1addd"
ACCOUNT_ADDRESS = "tccq9h7vnl68frvqapzv3tujrxtxtwqdnxw6yamrrgd"
ACCOUNT_PASSPHRASE = "satoshi"

address = sdk.rpc.account.import_raw(ACCOUNT_SECRET, ACCOUNT_PASSPHRASE)
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
```
