import inspect

import pytest

from codechain.primitives import AssetAddress
from codechain.primitives import H160
from codechain.primitives import MultiSig

validAddressString = "ccaqyqjmvml2hdp8s8xzqnr57r8ywtduy2u6gcq89vffl"
validAddress = AssetAddress.from_string(validAddressString)
invalidAddressString = "ccaqyqjmvml2hdp8s8xzqnr57r8ywtduy2u6gcq89vff"


def test_import():
    assert inspect.isclass(AssetAddress)
    assert inspect.isclass(MultiSig)


def test_check():
    assert AssetAddress.check(validAddressString)
    assert AssetAddress.check(validAddress)
    assert not AssetAddress.check(invalidAddressString)


def test_ensure():
    assert AssetAddress.ensure(validAddressString) == validAddress
    assert AssetAddress.ensure(validAddress) == validAddress


@pytest.mark.parametrize(
    "network_type, payload, network_id, version, should_throw",
    [
        (0, "0000000000000000000000000000000000000000", "tc", 1, False),
        (1, "0000000000000000000000000000000000000000", "tc", 1, False),
        (2, "0000000000000000000000000000000000000000", "tc", 1, False),
        (0, "0000000000000000000000000000000000000000", "tc", 0, True),
        (-1, "0000000000000000000000000000000000000000", "tc", 1, True),
        (4, "0000000000000000000000000000000000000000", "tc", 1, True),
        (255, "0000000000000000000000000000000000000000", "tc", 1, True),
    ],
)
def test_from_type_and_payload(
    network_type, payload, network_id, version, should_throw
):
    if should_throw:
        with pytest.raises(ValueError) as e:
            AssetAddress.from_type_and_payload(
                network_type, payload, network_id=network_id, version=version
            )
    else:
        try:
            AssetAddress.from_type_and_payload(
                network_type, payload, network_id=network_id, version=version
            )
        except Exception as e:  # noqa : E841
            raise pytest.fail(f"Unexpected exception: {e}")


def test_from_string_mutisig():
    address = AssetAddress.from_string(
        "tcaqypsyqg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyfzyg3zyg3zyg3zyg3zyg3zyg3zyg3zygsn28hf0"
    )
    payload = address.payload
    network_type = address.address_type

    assert network_type == 3

    n, m, pubkeys = payload

    assert n == 2
    assert m == 1

    assert pubkeys[0] == H160("1111111111111111111111111111111111111111")
    assert pubkeys[1] == H160("2222222222222222222222222222222222222222")


def test_from_type_and_payload_mutisig():
    sig = MultiSig(
        2,
        1,
        [
            H160("1111111111111111111111111111111111111111"),
            H160("2222222222222222222222222222222222222222"),
        ],
    )
    address1 = AssetAddress.from_string(
        "tcaqypsyqg3zyg3zyg3zyg3zyg3zyg3zyg3zyg3zyfzyg3zyg3zyg3zyg3zyg3zyg3zyg3zygsn28hf0"
    )
    address2 = AssetAddress.from_type_and_payload(3, sig, network_id="tc")

    assert address1.value == address2.value


def from_string():
    assert AssetAddress.from_string(validAddress) == validAddress
    with pytest.raises(ValueError):
        AssetAddress.from_string("cccqyqjmvml2hdp8s8xzqnr57r8ywtduy2u6gcq89vff")


def to_string():
    assert validAddress.to_string() == validAddressString
