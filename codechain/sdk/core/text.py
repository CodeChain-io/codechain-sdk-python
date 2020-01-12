from dataclasses import dataclass

from codechain.primitives import PlatformAddress


@dataclass
class TextJSON:
    content: str
    certifier: str


class Text:
    def __init__(self, content: str, certifier: PlatformAddress):
        self.content = content
        self.certifier = certifier

    @staticmethod
    def from_json(data: TextJSON):
        return Text(data.content, PlatformAddress.ensure(data.certifier))

    def to_json(self):
        return {"content": self.content, "certifier": str(self.certifier)}
