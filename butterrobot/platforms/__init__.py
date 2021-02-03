from functools import lru_cache

import structlog

from butterrobot.platforms.slack import SlackPlatform
from butterrobot.platforms.telegram import TelegramPlatform
from butterrobot.platforms.debug import DebugPlatform


logger = structlog.get_logger(__name__)
PLATFORMS = {
    platform.ID: platform
    for platform in (SlackPlatform, TelegramPlatform, DebugPlatform)
}


@lru_cache
def get_available_platforms():
    from butterrobot.platforms import PLATFORMS

    available_platforms = {}
    for platform in PLATFORMS.values():
        logger.debug("Setting up", platform=platform.ID)
        try:
            platform.init(app=None)
            available_platforms[platform.ID] = platform
            logger.info("platform setup completed", platform=platform.ID)
        except platform.PlatformInitError as error:
            logger.error("Platform init error", error=error, platform=platform.ID)
    return available_platforms
