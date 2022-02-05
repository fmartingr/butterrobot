from datetime import datetime

from butterrobot.plugins import Plugin
from butterrobot.objects import Message


class PingPlugin(Plugin):
    name = "Ping command"
    id = "contrib.dev.ping"

    @classmethod
    def on_message(cls, message, **kwargs):
        if message.text == "!ping":
            delta = datetime.now() - message.date
            delta_ms = delta.seconds * 1000 + delta.microseconds / 1000
            yield Message(
                chat=message.chat, reply_to=message.id, text=f"pong! ({delta_ms}ms)",
            )
