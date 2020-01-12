from ..core.transaction import Transaction
from .rpc import Rpc
from codechain.primitives import H256
from codechain.primitives import PlatformAddress
from codechain.primitives import U64


class AccountRpc:
    def __init__(self, rpc: Rpc):
        self.rpc = rpc

    def sign(
        self, message_digest: H256, address: PlatformAddress, passphrase: str = None
    ):
        if not H256.check(message_digest):
            raise ValueError(
                f"Expected the first argument to be an H256 value but found {message_digest}"
            )
        if not PlatformAddress.check(address):
            raise ValueError(
                f"Expected the second argument to be a PlatformAddress value but found {address}"
            )
        if passphrase is not None and not isinstance(passphrase, str):
            raise ValueError(
                f"Expected the third argument to be a string but found {passphrase}"
            )

        return self.rpc.send_rpc_request(
            "account",
            "sign",
            "0x" + str(H256(message_digest)),
            str(PlatformAddress.ensure(address)),
            passphrase,
        )

    def import_raw(self, secret: H256, passphrase: str = None):
        if not H256.check(secret):
            raise ValueError(
                f"Expected the first argument to be an H256 value but found {secret}"
            )
        if passphrase is not None and not isinstance(passphrase, str):
            raise ValueError(
                f"Expected the second argument to be a string but found {passphrase}"
            )

        result = self.rpc.send_rpc_request(
            "account", "import_raw", H256(secret).to_string(prefix=True)
        )

        return str(PlatformAddress.ensure(result))
