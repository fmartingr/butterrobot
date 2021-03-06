import random

import dice

from butterrobot.plugins import Plugin
from butterrobot.objects import Message


class LoquitoPlugin(Plugin):
    id = "contrib/fun/loquito"

    @classmethod
    def on_message(cls, message):
        if "lo quito" in message.text.lower():
            yield Message(chat=message.chat, reply_to=message.id, text="Loquito tu.",)


class DicePlugin(Plugin):
    id = "contrib/fun/dice"

    @classmethod
    def on_message(cls, message: Message):
        if message.text.startswith("!dice"):
            roll = int(dice.roll(message.text.replace("!dice ", "")))
            yield Message(chat=message.chat, reply_to=message.id, text=roll)


class CoinPlugin(Plugin):
    id = "contrib/fun/coin"

    @classmethod
    def on_message(cls, message: Message):
        if message.text.startswith("!coin"):
            yield Message(chat=message.chat, reply_to=message.id, text=random.choice(("heads", "tails")))
