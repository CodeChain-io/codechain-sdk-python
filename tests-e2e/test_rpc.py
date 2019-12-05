import binascii
import math
import re
import secrets
import time
from random import random

import pytest

from codechain.crypto import generate_private_key
from codechain.crypto import get_public_from_private
from codechain.crypto import sign_ecdsa
from codechain.rpc import Rpc


class TestBase:
    def test_ping(self):
        rpc = Rpc("http://localhost:8080", True)
        rpc.ping()

    def test_version(self):
        rpc = Rpc("http://localhost:8080", True)
        result = rpc.version()

        assert re.match("^[0-9]+.[0-9]+.[0-9]+$", result) is not None
        assert rpc.version() == result

    def test_commit_hash(self):
        rpc = Rpc("http://localhost:8080", True)
        result = rpc.commit_hash()

        assert re.match("^[a-fA-F0-9]{40}$", result) is not None
        assert rpc.commit_hash() == result


class TestAccout:
    def test_create(self):
        rpc = Rpc("http://localhost:8080", True)

        before_list = rpc.account.get_list()
        passphrase = f"some passphrase {random()}"
        account = rpc.account.create(passphrase)
        after_list = rpc.account.get_list()

        before_list.append(account)
        before_list.sort()
        after_list.sort()

        assert before_list == after_list

    def test_import_raw(self):
        rpc = Rpc("http://localhost:8080", True)

        before_list = rpc.account.get_list()
        passphrase = f"some passphrase {random()}"
        secret = generate_private_key()

        account = rpc.account.import_raw(
            "0x" + binascii.hexlify(secret).decode("ascii"), passphrase
        )
        after_list = rpc.account.get_list()

        before_list.append(account)
        before_list.sort()
        after_list.sort()

        assert before_list == after_list

    def test_sign(self):
        rpc = Rpc("http://localhost:8080", True)

        passphrase = f"some passphrase {random()}"
        secret = generate_private_key()

        account = rpc.account.import_raw(
            "0x" + binascii.hexlify(secret).decode("ascii"), passphrase
        )
        message = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

        signature = rpc.account.sign(message, account, passphrase)
        expected = sign_ecdsa(bytes.fromhex(message[2:]), secret)

        assert bytes.fromhex(signature[2:]) == expected

    def test_cannot_sign_without_passphrase(self):
        rpc = Rpc("http://localhost:8080", True)

        passphrase = f"some passphrase {random()}"
        secret = generate_private_key()

        account = rpc.account.import_raw(
            "0x" + binascii.hexlify(secret).decode("ascii"), passphrase
        )
        message = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

        with pytest.raises(Exception):
            rpc.account.sign(message, account, None)

    def test_unlock(self):
        rpc = Rpc("http://localhost:8080", True)

        passphrase = f"some passphrase {random()}"
        secret = generate_private_key()

        account = rpc.account.import_raw(
            "0x" + binascii.hexlify(secret).decode("ascii"), passphrase
        )
        message = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

        rpc.account.unlock(account, passphrase, None)

        signature = rpc.account.sign(message, account, None)
        expected = sign_ecdsa(bytes.fromhex(message[2:]), secret)

        assert bytes.fromhex(signature[2:]) == expected

    def test_unlock_with_duration(self):
        rpc = Rpc("http://localhost:8080", True)

        passphrase = f"some passphrase {random()}"
        secret = generate_private_key()

        account = rpc.account.import_raw(
            "0x" + binascii.hexlify(secret).decode("ascii"), passphrase
        )
        message = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

        rpc.account.unlock(account, passphrase, 1)

        signature = rpc.account.sign(message, account, None)
        expected = sign_ecdsa(bytes.fromhex(message[2:]), secret)

        assert bytes.fromhex(signature[2:]) == expected

        time.sleep(2)

        with pytest.raises(Exception):
            rpc.account.sign(message, account, None)

    def test_change_password(self):
        rpc = Rpc("http://localhost:8080", True)

        passphrase1 = f"some passphrase {random()}"
        passphrase2 = f"another passphrase {random()}"

        secret = generate_private_key()

        account = rpc.account.import_raw(
            "0x" + binascii.hexlify(secret).decode("ascii"), passphrase1
        )

        message = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"

        signature1 = rpc.account.sign(message, account, passphrase1)
        expected = sign_ecdsa(bytes.fromhex(message[2:]), secret)

        assert bytes.fromhex(signature1[2:]) == expected

        with pytest.raises(Exception):
            rpc.account.sign(message, account, passphrase2)

        rpc.account.change_password(account, passphrase1, passphrase2)

        with pytest.raises(Exception):
            rpc.account.sign(message, account, passphrase1)

        signature2 = rpc.account.sign(message, account, passphrase2)

        assert bytes.fromhex(signature2[2:]) == expected


class TestChain:
    def test_network_id(self):
        rpc = Rpc("http://localhost:8080", True)

        network_id = rpc.chain.get_network_id()

        assert network_id == "tc"

    def test_genesis_accounts(self):
        rpc = Rpc("http://localhost:8080", True)
        accounts = rpc.chain.get_genesis_accounts()

        expected = [
            "tccqyqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqyca3rwt",
            "tccqyqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqgfrhflv",
            "tccqyqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvxf40sk",
            "tccqyqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqszkma5z",
            "tccqyqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq5duemmc",
            "tccqyqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqcuzl32l",
            "tccqyqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqungah99",
            "tccqyqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqpqc2ul2h",
            "tccq9h7vnl68frvqapzv3tujrxtxtwqdnxw6yamrrgd",
            "tccq8vapdlstar6ghmqgczp6j2e83njsqq0tsvaxm9u",
        ]

        expected.sort()
        accounts.sort()

        assert accounts == expected

    def test_number_of_shards(self):
        rpc = Rpc("http://localhost:8080", True)
        number_of_shards = rpc.chain.get_number_of_shards(0)

        assert number_of_shards == 1


class TestDevel:
    def test_cnannot_use_by_default(self):
        rpc = Rpc("http://localhost:8080")

        assert not hasattr(rpc, "devel")

    def test_does_not_exist_when_it_is_explicitly_false(self):
        rpc = Rpc("http://localhost:8080", False)

        assert not hasattr(rpc, "devel")

    def test_exist(self):
        rpc = Rpc("http://localhost:8080", True)

        assert hasattr(rpc, "devel")

    def test_get_block_sync_peers(self):
        rpc = Rpc("http://localhost:8080", True)

        assert rpc.devel.get_block_sync_peers() == []

    def test_tps(self):
        rpc = Rpc("http://localhost:8080", True)
        tps = rpc.devel.test_tps(1, 0, "payOnly")

        assert tps != 0

    def test_trie(self):
        rpc = Rpc("http://localhost:8080", True)
        devel = rpc.devel

        keys1 = devel.get_state_trie_keys(0, 3)
        assert len(keys1) == 3

        for key in keys1:
            value = devel.get_state_trie_value(key)
            assert value is not None

        keys2 = devel.get_state_trie_keys(3, 10)
        assert len(keys2) == 10

        for key in keys2:
            value = devel.get_state_trie_value(key)
            assert value is not None

        for key1 in keys1:
            for key2 in keys2:
                assert key1 != key2


class TestEngine:
    def test_coinbase(self):
        rpc = Rpc("http://localhost:8080", True)
        coinbase = rpc.engine.get_coinbase()

        assert coinbase is None

    def test_block_reward(self):
        rpc = Rpc("http://localhost:8080", True)
        reward = rpc.engine.get_block_reward(0)

        assert reward == 0

    def test_recommended_confirmation(self):
        rpc = Rpc("http://localhost:8080", True)
        confirmation = rpc.engine.get_recommended_confirmation()

        assert confirmation == 1


class TestMempool:
    def test_error_hint(self):
        rpc = Rpc("http://localhost:8080", True)
        transaction_hash = f"0x{secrets.token_hex(32)}"
        hint = rpc.mempool.get_error_hint(transaction_hash)

        assert hint is None

    def test_transaction_results_by_tracker(self):
        rpc = Rpc("http://localhost:8080", True)
        tracker = f"0x{secrets.token_hex(32)}"
        results = rpc.mempool.get_transaction_results_by_tracker(tracker)

        assert results == []

    def test_pending_transactions(self):
        rpc = Rpc("http://localhost:8080", True)
        result = rpc.mempool.get_pending_transactions(None, None)

        assert result["transactions"] == []
        assert result["lastTimestamp"] is None


class TestNet:
    def random_ip(self, len: int = 4):
        first = 0 if len < 1 else 1 + math.floor(random() * 254)
        second = 0 if len < 2 else math.floor(random() * 256)
        third = 0 if len < 3 else math.floor(random() * 256)
        fourth = 0 if len < 4 else math.floor(random() * 254)

        return f"{first}.{second}.{third}.{fourth}"

    def random_port(self):
        return 49152 + math.floor(random() * (65535 - 49152))

    def test_register_remote_key(self):
        rpc = Rpc("http://localhost:8080", True)
        address = self.random_ip()
        port = self.random_port()
        remote_public_key = get_public_from_private(generate_private_key())
        local = rpc.net.register_remote_key_for(
            address, port, "0x" + binascii.hexlify(remote_public_key).decode("ascii")
        )

        assert rpc.net.locak_key_for(address, port) == local

    def test_port(self):
        rpc = Rpc("http://localhost:8080", True)
        port = rpc.net.get_port()

        assert port == 3485

    def test_peer_count(self):
        rpc = Rpc("http://localhost:8080", True)
        count = rpc.net.get_peer_count()

        assert count == 0

    def test_established_peers(self):
        rpc = Rpc("http://localhost:8080", True)
        peers = rpc.net.get_establiched_peers()

        assert peers == []

    def test_recent_usage(self):
        rpc = Rpc("http://localhost:8080", True)
        usage = rpc.net.recent_network_usage()

        assert usage == {}

    def test_whitelist_add(self):
        rpc = Rpc("http://localhost:8080", True)
        results = rpc.net.get_whitelist()
        whitelist = results["list"]
        enabled = results["enabled"]

        if enabled:
            rpc.net.disableWhitelist()

        for [address, _tag] in whitelist:
            rpc.net.remove_from_whitelist(address)

        while True:
            results = rpc.net.get_whitelist()
            whitelist = results["list"]
            enabled = results["enabled"]
            if not enabled and len(whitelist) == 0:
                break
            time.sleep(0.3)

        expected = []

        address = f"{self.random_ip(2)}/16"
        tag = "e2e test"
        rpc.net.add_to_whitelist(address, tag)
        expected.append([address, tag])

        results = rpc.net.get_whitelist()
        whitelist = results["list"]
        enabled = results["enabled"]

        assert enabled is False
        assert whitelist == expected

        address = f"{self.random_ip(3)}/24"
        tag = "e2e test2"
        rpc.net.add_to_whitelist(address, tag)
        expected.append([address, tag])

        results = rpc.net.get_whitelist()
        whitelist = results["list"]
        enabled = results["enabled"]

        assert enabled is False
        whitelist.sort()
        expected.sort()
        assert whitelist == expected

    def test_whitelist_enable(self):
        rpc = Rpc("http://localhost:8080", True)
        results = rpc.net.get_whitelist()
        whitelist = results["list"]
        enabled = results["enabled"]

        if enabled:
            rpc.net.disableWhitelist()

        for [address, _tag] in whitelist:
            rpc.net.remove_from_whitelist(address)

        while True:
            results = rpc.net.get_whitelist()
            whitelist = results["list"]
            enabled = results["enabled"]
            if not enabled and len(whitelist) == 0:
                break
            time.sleep(0.3)

        results = rpc.net.get_whitelist()
        enabled = results["enabled"]

        assert enabled is False

        rpc.net.enable_whitelist()

        results = rpc.net.get_whitelist()
        enabled = results["enabled"]

        assert enabled is True

    def test_blacklist_add(self):
        rpc = Rpc("http://localhost:8080", True)
        results = rpc.net.get_blacklist()
        blacklist = results["list"]
        enabled = results["enabled"]

        if enabled:
            rpc.net.disable_blacklist()

        for [address, _tag] in blacklist:
            rpc.net.remove_from_blacklist(address)

        while True:
            results = rpc.net.get_blacklist()
            blacklist = results["list"]
            enabled = results["enabled"]
            if not enabled and len(blacklist) == 0:
                break
            time.sleep(0.3)

        expected = []

        address = f"{self.random_ip(2)}/16"
        tag = "e2e test"
        rpc.net.add_to_blacklist(address, tag)
        expected.append([address, tag])

        results = rpc.net.get_blacklist()
        blacklist = results["list"]
        enabled = results["enabled"]

        assert enabled is False
        assert blacklist == expected

        address = f"{self.random_ip(3)}/24"
        tag = "e2e test2"
        rpc.net.add_to_blacklist(address, tag)
        expected.append([address, tag])

        results = rpc.net.get_blacklist()
        blacklist = results["list"]
        enabled = results["enabled"]

        assert enabled is False
        blacklist.sort()
        expected.sort()
        assert blacklist == expected

    def test_blacklist_enable(self):
        rpc = Rpc("http://localhost:8080", True)
        results = rpc.net.get_blacklist()
        blacklist = results["list"]
        enabled = results["enabled"]

        if enabled:
            rpc.net.disable_blacklist()

        for [address, _tag] in blacklist:
            rpc.net.remove_from_blacklist(address)

        while True:
            results = rpc.net.get_blacklist()
            blacklist = results["list"]
            enabled = results["enabled"]
            if not enabled and len(blacklist) == 0:
                break
            time.sleep(0.3)

        results = rpc.net.get_blacklist()
        enabled = results["enabled"]

        assert enabled is False

        rpc.net.enable_blacklist()

        results = rpc.net.get_blacklist()
        enabled = results["enabled"]

        assert enabled is True
