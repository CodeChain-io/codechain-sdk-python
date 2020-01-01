import binascii
from dataclasses import dataclass
from typing import List

from ..key.p2pkh import P2PKH
from ..key.p2pkhburn import P2PKHBurn
from codechain.primitives import AssetAddress
from codechain.primitives import H160
from codechain.primitives import U64


@dataclass
class AssetMintOutputJSON:
    lock_script_hash: str
    parameters: List[str]
    supply: str


class AssetMintOutput:
    def __init__(
        self,
        supply: U64,
        lock_script_hash: H160 = None,
        paramters: bytes = None,
        recipient: AssetAddress = None,
    ):
        if recipient is not None:
            address_type = recipient.address_type
            payload = recipient.payload
            if "pubkeys" in payload:
                raise ValueError("Multisig payload is not supported yet")

            if address_type == 0x00:
                self.lock_script_hash = payload
                self.parameters = []
            elif address_type == 0x01:
                self.lock_script_hash = P2PKH.get_lock_script_hash()
                self.parameters = [payload]
            elif address_type == 0x02:
                self.lock_script_hash = P2PKHBurn.get_lock_script_hash()
                self.parameters = [payload]
            else:
                raise ValueError(
                    f"Unexpected type of AssetAddress: {address_type}, {recipient}"
                )
        else:
            self.lock_script_hash = lock_script_hash
            self.parameters = paramters

        self.supply = supply

    @staticmethod
    def from_json(data: AssetMintOutputJSON):
        return AssetMintOutput(
            U64(data["supply"]),
            H160(data["lockScriptHash"]),
            map(lambda x: bytes.fromhex(x), data["parameters"]),
        )

    def to_json(self):
        return {
            "lockScriptHash": self.lock_script_hash.to_json(),
            "parameters": map(lambda x: binascii.hexlify(x).decode("ascii")),
            "supply": self.supply.to_json(),
        }
