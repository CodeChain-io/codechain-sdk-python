import pytest

from codechain.primitives import H160
from codechain.primitives import PlatformAddress

account_id = H160("7b5e0ee8644c6f585fc297364143280a45844502")
account_id_string = "7b5e0ee8644c6f585fc297364143280a45844502"
mainnet_address = "cccq9a4urhgv3xx7kzlc2tnvs2r9q9ytpz9qgs7q0a7"
testnet_address = "tccq9a4urhgv3xx7kzlc2tnvs2r9q9ytpz9qgcejvw8"


class TestFromAccountId:
    def test_mainnet(self):
        address = PlatformAddress.from_account_id(account_id, network_id="cc")

        assert address.value == "cccq9a4urhgv3xx7kzlc2tnvs2r9q9ytpz9qgs7q0a7"

    def test_testnet(self):
        address = PlatformAddress.from_account_id(account_id, network_id="tc")

        assert address.value == "tccq9a4urhgv3xx7kzlc2tnvs2r9q9ytpz9qgcejvw8"

    def test_valid_version(self):
        try:
            PlatformAddress.from_account_id(account_id, network_id="tc", version=1)
        except Exception as e:
            raise pytest.fail(f"Unexpected exception: {e}")

    def test_invalid_version(self):
        with pytest.raises(ValueError) as e:
            PlatformAddress.from_account_id(account_id, network_id="tc", version=99)
        assert "version" in str(e.value)

    def test_invalid_network_id(self):
        with pytest.raises(ValueError) as e:
            PlatformAddress.from_account_id(account_id, network_id="x", version=1)
        assert "network_id" in str(e.value)

    def test_invalid_account_id(self):
        with pytest.raises(ValueError) as e:
            PlatformAddress.from_account_id("xxx", network_id="tc")
        assert "account_id" in str(e.value)


class TestFromString:
    def test_mainnet(self):
        address = PlatformAddress.from_string(mainnet_address)

        assert address.account_id == account_id

    def test_testnet(self):
        address = PlatformAddress.from_string(testnet_address)

        assert address.account_id == account_id

    def test_invalid_checksum(self):
        invalid_checksum_address = "cccqpa4urhgv3xx7kzlc2tnvs2r9q9ytpz9qgqqqqqq"

        with pytest.raises(ValueError) as e:
            PlatformAddress.from_string(invalid_checksum_address)
        assert "checksum" in str(e.value)
