import hashlib
from typing import Union

import dataset

from butterrobot.config import SECRET_KEY, DATABASE_PATH
from butterrobot.objects import User, Channel, ChannelPlugin

db = dataset.connect(DATABASE_PATH)


class Query:
    class NotFound(Exception):
        pass

    class Duplicated(Exception):
        pass

    @classmethod
    def all(cls):
        """
        Iterate over all rows on a table.
        """
        for row in db[cls.tablename].all():
            yield cls.obj(**row)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns the object representation of an specific row in a table.
        Allows retrieving object by multiple columns.
        Raises `NotFound` error if query return no results.
        """
        row = db[cls.tablename].find_one(**kwargs)
        if not row:
            raise cls.NotFound
        return cls.obj(**row)

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a new row in the table with the provided arguments.
        Returns the row_id
        TODO: Return obj?
        """
        return db[cls.tablename].insert(kwargs)

    @classmethod
    def exists(cls, **kwargs) -> bool:
        """
        Check for the existence of a row with the provided columns.
        """
        try:
            cls.get(**kwargs)
        except cls.NotFound:
            return False
        return True

    @classmethod
    def update(cls, row_id, **fields):
        fields.update({"id": row_id})
        return db[cls.tablename].update(fields, ("id",))

    @classmethod
    def delete(cls, id):
        return db[cls.tablename].delete(id=id)


class UserQuery(Query):
    tablename = "users"
    obj = User

    @classmethod
    def _hash_password(cls, password):
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), str.encode(SECRET_KEY), 100000
        ).hex()

    @classmethod
    def check_credentials(cls, username, password) -> Union[User, "False"]:
        user = db[cls.tablename].find_one(username=username)
        if user:
            hash_password = cls._hash_password(password)
            if user["password"] == hash_password:
                return cls.obj(**user)
        return False

    @classmethod
    def create(cls, **kwargs):
        kwargs["password"] = cls._hash_password(kwargs["password"])
        return super().create(**kwargs)


class ChannelQuery(Query):
    tablename = "channels"
    obj = Channel

    @classmethod
    def create(cls, platform, platform_channel_id, enabled=False, channel_raw={}):
        params = {
            "platform": platform,
            "platform_channel_id": platform_channel_id,
            "enabled": enabled,
            "channel_raw": channel_raw,
        }
        super().create(**params)
        return cls.obj(**params)

    @classmethod
    def get(cls, _id):
        channel = super().get(id=_id)
        plugins = ChannelPluginQuery.get_from_channel_id(_id)
        channel.plugins = {plugin.plugin_id: plugin for plugin in plugins}
        return channel

    @classmethod
    def get_by_platform(cls, platform, platform_channel_id):
        result = db[cls.tablename].find_one(
            platform=platform, platform_channel_id=platform_channel_id
        )
        if not result:
            raise cls.NotFound

        plugins = ChannelPluginQuery.get_from_channel_id(result["id"])

        return cls.obj(
            plugins={plugin.plugin_id: plugin for plugin in plugins}, **result
        )

    @classmethod
    def delete(cls, _id):
        ChannelPluginQuery.delete_by_channel(channel_id=_id)
        super().delete(_id)


class ChannelPluginQuery(Query):
    tablename = "channel_plugin"
    obj = ChannelPlugin

    @classmethod
    def create(cls, channel_id, plugin_id, enabled=False, config={}):
        if cls.exists(id=channel_id, plugin_id=plugin_id):
            raise cls.Duplicated

        params = {
            "channel_id": channel_id,
            "plugin_id": plugin_id,
            "enabled": enabled,
            "config": config,
        }
        obj_id = super().create(**params)
        return cls.obj(id=obj_id, **params)

    @classmethod
    def get_from_channel_id(cls, channel_id):
        yield from [
            cls.obj(**row) for row in db[cls.tablename].find(channel_id=channel_id)
        ]

    @classmethod
    def delete_by_channel(cls, channel_id):
        channel_plugins = cls.get_from_channel_id(channel_id)
        [cls.delete(item.id) for item in channel_plugins]
