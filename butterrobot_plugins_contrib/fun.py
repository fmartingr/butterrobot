import random

import dice
import structlog

from butterrobot.plugins import Plugin
from butterrobot.objects import Message


logger = structlog.get_logger(__name__)


class LoquitoPlugin(Plugin):
    name = "Loquito reply"
    id = "contrib.fun.loquito"

    @classmethod
    def on_message(cls, message, **kwargs):
        if "lo quito" in message.text.lower():
            yield Message(chat=message.chat, reply_to=message.id, text="Loquito tu.",)


class DicePlugin(Plugin):
    name = "Dice command"
    id = "contrib.fun.dice"
    DEFAULT_FORMULA = "1d20"

    @classmethod
    def on_message(cls, message: Message, **kwargs):
        if message.text.startswith("!dice"):
            dice_formula = message.text.replace("!dice", "").strip()
            if not dice_formula:
                dice_formula = cls.DEFAULT_FORMULA
            roll = int(dice.roll(dice_formula))
            yield Message(chat=message.chat, reply_to=message.id, text=roll)


class CoinPlugin(Plugin):
    name = "Coin command"
    id = "contrib.fun.coin"

    @classmethod
    def on_message(cls, message: Message, **kwargs):
        if message.text.startswith("!coin"):
            yield Message(chat=message.chat, reply_to=message.id, text=random.choice(("heads", "tails")))
