from butterrobot.platforms.slack import SlackPlatform
from butterrobot.platforms.telegram import TelegramPlatform


PLATFORMS = {platform.ID: platform for platform in (SlackPlatform, TelegramPlatform,)}
