from ../Hexstring import H160
from typing import Tuple, Union


class AssetAddress():
    def __init__(self, addressType: int, payload: Union[H160, str, Tuple], address: str):
        self.addressType = addressType
        if type(payload) is H160 or type(payload) is str:
            self.payload = H160(payload)
        else:
            m, n, pubkeys = payload
            self.payload = (m, n, list(map(lambda p: H160(p), pubkeys)))
        self.value = address
