class Script(bytes):
    Opcode = {
        "NOP": 0x00,
        "BURN": 0x01,
        "SUCCESS": 0x02,
        "FAIL": 0x03,
        "NOT": 0x10,
        "EQ": 0x11,
        "JMP": 0x20,
        "JNZ": 0x21,
        "JZ": 0x22,
        "PUSH": 0x30,
        "POP": 0x31,
        "PUSHB": 0x32,
        "DUP": 0x33,
        "SWAP": 0x34,
        "COPY": 0x35,
        "DROP": 0x36,
        "CHKSIG": 0x80,
        "CHKMULTISIG": 0x81,
        "BLAKE256": 0x90,
        "SHA256": 0x91,
        "RIPEMD160": 0x92,
        "KECCAK256": 0x93,
        "BLAKE160": 0x94,
        "BLKNUM": 0xA0,
        "CHKTIMELOCK": 0xB0,
    }

    @staticmethod
    def empty():
        return Script(bytes())
