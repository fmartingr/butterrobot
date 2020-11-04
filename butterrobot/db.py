import hashlib
import os

import dataset

from butterrobot.config import DATABASE_PATH, SECRET_KEY

db = dataset.connect(DATABASE_PATH)


class Model:
    class NotFound(Exception):
        pass

class User(Model):
    _table = db["users"]

    @classmethod
    def _hash_password(cls, password):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), str.encode(SECRET_KEY), 100000).hex()

    @classmethod
    def check_credentials(cls, username, password):
        try:
            user = cls.get(username=username)
            hash_password = cls._hash_password(password)
            if user["password"] == hash_password:
                return user
        except cls.NotFound:
            pass
        return False

    @classmethod
    def create(cls, username, password):
        hash_password = cls._hash_password(password)
        cls._table.insert({"username": username, "password": hash_password})

    @classmethod
    def get(cls, username):
        result = cls._table.find_one(username=username)
        if not result:
            raise cls.NotFound
        return result

    @classmethod
    def delete(cls, username):
        return cls._table.delete(username=username)

    @classmethod
    def update(cls, username, **fields):
        fields.update({"username": username})
        return cls._table.update(fields, ["username"])


class Channel(Model):
    _table = db["channels"]

    @classmethod
    def create(cls, provider, channel_id, enabled=False, channel_raw={}):
        cls._table.insert({"provider": provider, "channel_id": channel_id, "enabled": enabled, "channel_raw": channel_raw})

    @classmethod
    def get(cls, username):
        result = cls._table.find_one(username=username)
        if not result:
            raise cls.UserNotFound
        return result

    @classmethod
    def delete(cls, username):
        return cls._table.delete(username=username)

    @classmethod
    def update(cls, username, **fields):
        fields.update({"username": username})
        return cls._table.update(fields, ["username"])
