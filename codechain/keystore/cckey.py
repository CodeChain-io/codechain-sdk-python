from jsondb.db import Database

from .keystoremanager import keystoreManager
from .keytype import KeyType


class CCkey:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.db.data(
            dictionary={"meta": "", "platform": [], "asset": [], "hdwseed": []}
        )
        self.platform = keystoreManager(KeyType.PLATFORM, self.db)
        self.asset = keystoreManager(KeyType.ASSET, self.db)

    @staticmethod
    def create(**kwargs):
        db_path = kwargs.get("db_path", "keystore.db")

        return CCkey(db_path)

    def exist(self, **kwargs):
        db_path = kwargs.get("db_path", "keystore.db")
        db = Database(db_path)

        meta = db["meta"]
        platform = db["platform"]
        asset = db["asset"]
        hdwseed = db["hdwseed"]

        return (
            (meta is not None and meta != "")
            or (platform is not None and len(platform) != 0)
            or (asset is not None and len(asset) != 0)
            or (hdwseed is not None and len(hdwseed) != 0)
        )

    def get_meta(self):
        return self.db["meta"]

    def set_meta(self, meta: str):
        self.db["meta"] = meta
        return
