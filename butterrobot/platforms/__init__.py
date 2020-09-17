from butterrobot.platforms.slack import SlackPlatform
from butterrobot.platforms.telegram import TelegramPlatform
from butterrobot.platforms.debug import DebugPlatform


PLATFORMS = {platform.ID: platform for platform in (SlackPlatform, TelegramPlatform, DebugPlatform)}
