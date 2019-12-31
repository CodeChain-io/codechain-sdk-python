from dataclasses import dataclass
from typing import List
from typing import Union

from .assetoutpoint import AssetOutPoint
from .assetoutpoint import AssetOutPointJSON


@dataclass
class Timelock:
    lock_type: str
    value: int


@dataclass
class AssetTransferInputJSON:
    prev_out: AssetOutPointJSON
    timelock: Union[None, Timelock]
    lock_script: List[int]
    unlock_script: List[int]


class AssetTransferInput:
    def __init__(
        self,
        prev_out: AssetOutPoint,
        timelock: Union[Timelock, None],
        lock_script: Union[bytearray, bytes] = b"",
        unlock_script: Union[bytearray, bytes] = b"",
    ):
        self.prev_out = prev_out
        self.timelock = timelock
        self.lock_script = lock_script
        self.unlock_script = unlock_script

    @staticmethod
    def from_json(data: AssetTransferInputJSON):
        return AssetTransferInput(
            AssetOutPoint.from_json(data.prev_out),
            data.timelock,
            bytes(data.lock_script),
            bytes(data.unlock_script),
        )

    def to_encode_object(self):
        return [
            self.prev_out.to_encode_object(),
            convert_timelock_to_encode_object(self.timelock),
            self.lock_script,
            self.unlock_script,
        ]

    def to_json(self):
        return {
            "prevOut": self.prev_out.to_json(),
            "timelock": self.timelock,
            "lockScript": list(self.lock_script),
            "unlockScript": list(self.unlock_script),
        }

    def without_script(self):
        return AssetTransferInput(self.prev_out, self.timelock, bytes(), bytes())


def convert_timelock_to_encode_object(timelock: Union[Timelock, None]):
    if timelock is None:
        return []

    lock_type = timelock.lock_type
    value = timelock.value
    if lock_type == "block":
        type_encoded = 1
    elif lock_type == "blockAge":
        type_encoded = 2
    elif lock_type == "time":
        type_encoded = 3
    elif lock_type == "timeAge":
        type_encoded = 4
    else:
        raise ValueError(f"Unexpected timelock type: {lock_type}")

    return [[type_encoded, value]]
