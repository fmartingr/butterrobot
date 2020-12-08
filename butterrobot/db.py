import hashlib
import os

import dataset

from butterrobot.config import DATABASE_PATH, SECRET_KEY
from butterrobot.objects import Channel, ChannelPlugin, User

db = dataset.connect(DATABASE_PATH)



class Query:
    class NotFound(Exception):
        pass

    class Duplicated(Exception):
        pass

    @classmethod
    def all(cls):
        for row in cls._table.all():
            yield cls._obj(**row)

    @classmethod
    def exists(cls, *args, **kwargs):
        try:
            # Using only *args since those are supposed to be mandatory
            cls.get(*args)
        except cls.NotFound:
            return False
        return True

    @classmethod
    def update(cls, row_id, **fields):
        fields.update({"id": row_id})
        return cls._table.update(fields, ("id", ))

    @classmethod
    def get(cls, _id):
        row = cls._table.find_one(id=_id)
        if not row:
            raise cls.NotFound
        return cls._obj(**row)

    @classmethod
    def update(cls, _id, **fields):
        fields.update({"id": _id})
        return cls._table.update(fields, ("id"))

    @classmethod
    def delete(cls, _id):
        cls._table.delete(id=_id)

class UserQuery(Query):
    _table = db["users"]
    _obj = User

    @classmethod
    def _hash_password(cls, password):
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), str.encode(SECRET_KEY), 100000
        ).hex()

    @classmethod
    def check_credentials(cls, username, password):
        user = cls._table.find_one(username=username)
        if user:
            hash_password = cls._hash_password(password)
            if user["password"] == hash_password:
                return cls._obj(**user)
        return False

    @classmethod
    def create(cls, username, password):
        hash_password = cls._hash_password(password)
        cls._table.insert({"username": username, "password": hash_password})

    @classmethod
    def delete(cls, username):
        return cls._table.delete(username=username)

    @classmethod
    def update(cls, username, **fields):
        fields.update({"username": username})
        return cls._table.update(fields, ("username",))


class ChannelQuery(Query):
    _table = db["channels"]
    _obj = Channel

    @classmethod
    def create(cls, platform, platform_channel_id, enabled=False, channel_raw={}):
        params = {
            "platform": platform,
            "platform_channel_id": platform_channel_id,
            "enabled": enabled,
            "channel_raw": channel_raw,
        }
        cls._table.insert(params)
        return cls._obj(**params)

    @classmethod
    def get(cls, _id):
        channel = super().get(_id)
        plugins = ChannelPluginQuery.get_from_channel_id(_id)
        channel.plugins = {plugin.plugin_id: plugin for plugin in plugins}
        return channel

    @classmethod
    def get_by_platform(cls, platform, platform_channel_id):
        result = cls._table.find_one(
            platform=platform, platform_channel_id=platform_channel_id
        )
        if not result:
            raise cls.NotFound

        plugins = ChannelPluginQuery.get_from_channel_id(result["id"])

        return cls._obj(plugins={plugin.plugin_id: plugin for plugin in plugins}, **result)

    @classmethod
    def delete(cls, _id):
        ChannelPluginQuery.delete_by_channel(channel_id=_id)
        super().delete(_id)


class ChannelPluginQuery(Query):
    _table = db["channel_plugin"]
    _obj = ChannelPlugin

    @classmethod
    def create(cls, channel_id, plugin_id, enabled=False, config={}):
        if cls.exists(channel_id, plugin_id):
            raise cls.Duplicated

        params = {
            "channel_id": channel_id,
            "plugin_id": plugin_id,
            "enabled": enabled,
            "config": config,
        }
        obj_id = cls._table.insert(params)
        return cls._obj(id=obj_id, **params)

    @classmethod
    def get(cls, channel_id, plugin_id):
        result = cls._table.find_one(channel_id=channel_id, plugin_id=plugin_id)
        if not result:
            raise cls.NotFound
        return cls._obj(**result)

    @classmethod
    def get_from_channel_id(cls, channel_id):
        yield from [cls._obj(**row) for row in cls._table.find(channel_id=channel_id)]

    @classmethod
    def delete(cls, channel_plugin_id):
        return cls._table.delete(id=channel_plugin_id)

    @classmethod
    def delete_by_channel(cls, channel_id):
        cls._table.delete(channel_id=channel_id)

