from datetime import datetime

from butterrobot.plugins import Plugin
from butterrobot.objects import Message


class PingPlugin(Plugin):
    id = "contrib/dev/ping"

    @classmethod
    async def on_message(cls, message):
        if message.text == "!ping":
            delta = datetime.now() - message.date
            delta_ms = delta.seconds * 1000 + delta.microseconds / 1000
            return Message(
                chat=message.chat, reply_to=message.id, text=f"pong! ({delta_ms}ms)",
            )
