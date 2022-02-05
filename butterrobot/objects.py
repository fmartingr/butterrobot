from datetime import datetime
from dataclasses import dataclass, field
from typing import Text, Optional, Dict

import structlog


logger = structlog.get_logger(__name__)


@dataclass
class ChannelPlugin:
    id: int
    channel_id: int
    plugin_id: str
    enabled: bool = False
    config: dict = field(default_factory=dict)


@dataclass
class Channel:
    platform: str
    platform_channel_id: str
    channel_raw: dict
    enabled: bool = False
    id: Optional[int] = None
    plugins: Dict[str, ChannelPlugin] = field(default_factory=dict)

    def has_enabled_plugin(self, plugin_id):
        if plugin_id not in self.plugins:
            logger.debug("No enabled!", plugin_id=plugin_id, plugins=self.plugins)
            return False

        return self.plugins[plugin_id].enabled

    @property
    def channel_name(self):
        from butterrobot.platforms import PLATFORMS

        return PLATFORMS[self.platform].parse_channel_name_from_raw(self.channel_raw)


@dataclass
class Message:
    text: Text
    chat: Text
    # TODO: Move chat references to `.channel.platform_channel_id`
    channel: Optional[Channel] = None
    author: Text = None
    from_bot: bool = False
    date: Optional[datetime] = None
    id: Optional[Text] = None
    reply_to: Optional[Text] = None
    raw: dict = field(default_factory=dict)


@dataclass
class User:
    id: int
    username: Text
    password: Text
