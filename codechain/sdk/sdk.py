from typing import List

from .core import Core
from .key import KeyStoreType
from .rpc import Rpc
from .utils import blake128
from .utils import blake128_with_key
from .utils import blake160
from .utils import blake160_with_key
from .utils import blake256
from .utils import blake256_with_key
from .utils import generate_private_key
from .utils import get_account_id_from_public
from .utils import get_public_from_private
from .utils import recover_ecdsa
from .utils import ripemd160
from .utils import sign_ecdsa
from .utils import verify_ecdsa


class SDK:
    Rpc = Rpc
    Core = Core

    def __init__(
        self,
        server: str,
        key_store_type: KeyStoreType = None,
        network_id: str = None,
        transaction_signer: str = None,
        fallback_servers: List[str] = None,
    ):
        if key_store_type is None:
            key_store_type = KeyStoreType("local", None)
        if network_id is None:
            network_id = "tc"

        self.rpc = Rpc(server, transaction_signer, fallback_servers)
        self.core = Core(network_id)
        self.network_id = network_id
