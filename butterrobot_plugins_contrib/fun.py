from butterrobot.plugins import Plugin
from butterrobot.objects import Message


class LoquitoPlugin(Plugin):
    id = "contrib/fun/loquito"

    @classmethod
    async def on_message(cls, message):
        if "lo quito" in message.text.lower():
            return Message(chat=message.chat, reply_to=message.id, text="Loquito tu.",)
