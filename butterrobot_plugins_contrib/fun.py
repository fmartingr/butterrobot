import dice

from butterrobot.plugins import Plugin
from butterrobot.objects import Message


class LoquitoPlugin(Plugin):
    id = "contrib/fun/loquito"

    @classmethod
    async def on_message(cls, message):
        if "lo quito" in message.text.lower():
            yield Message(chat=message.chat, reply_to=message.id, text="Loquito tu.",)


class DicePlugin(Plugin):
    id = "contrib/fun/dice"

    @classmethod
    async def on_message(cls, message: Message):
        if message.text.startswith("!dice"):
            roll = int(dice.roll(message.text.replace("!dice ", "")))
            yield Message(chat=message.chat, reply_to=message.id, text=roll)