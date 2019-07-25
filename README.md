# CodeChain SDK for Python

A Python SDK for CodeChain.

## API Documentation (For SDK users)

Not prepared

## Getting Started (For SDK developers)

Not prepared

## Submodules

### codechain-crypto

Python implementation of crypto functions and classes used in CodeChain.

#### Functions

* sign_schnorr
* verify_schnorr
* recover_schnorr

* sign_ecdsa
* verify_ecdsa
* recover_ecdsa
* blake256, blake256_with_key, blake160, blake160_with_key, blake128, blake128_with_key
* ripemd160
* get_public_from_private
* generate_private_key

### codechain-rpc

codechain-rpc is a Python module that calls RPC to a CodeChain node.

#### RPC list

You can find the RPC list in [this link](https://github.com/CodeChain-io/codechain/blob/master/spec/JSON-RPC.md).

### codechain-primitives

Python functions and classes for CodeChain's primitives.

#### Functions

* to_hex
* get_account_id_from_private
* get_account_id_from_public
* to_locale_string

#### Classes

* H128, H160, H256, H512
* U64, U128, U256
* AssetAddres
* PlatformAddress

### codechain-keystore

codechain-keystore is a private key management module. It saves CodeChain's asset transfer address safely in a disk. If you want to manage CodeChain keys using python, you should use this.

#### How your private key is saved

We use a JSON file to save an encrypted private key. You can find the file in `./keystore.db`.

## Submitting patches
- Use `Black`_ to autoformat your code. This should be done for you as a git `pre-commit`_ hook.
### First time setup
- Clone your GitHub fork locally:
- Add the main repository as a remote to update later:
- Create a virtualenv using pipenv:
```shell
$ pipenv install --dev
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
