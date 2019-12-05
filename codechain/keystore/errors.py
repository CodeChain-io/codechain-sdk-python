from enum import Enum


class ErrorCode(Enum):
    UNKNOWN = 0
    NOSUCHKEY = 1
    NOSUCHSEEDHASH = 2
    DECRYPTIONFAILED = 3
    DBERROR = 4
    WRONGSEEDLENGTH = 5
    WRONGMNEMONICSTRING = 6


class KeystoreError(Exception):
    def __init__(self, code: ErrorCode):
        super().__init__(str(code.name))

        self.code = code
        self.code_name = str(code.name)
        self.name = "KeystoreError"
