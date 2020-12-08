import traceback
import pkg_resources
from abc import abstractclassmethod
from functools import lru_cache
from typing import Optional, Dict

import structlog

from butterrobot.objects import Message

logger = structlog.get_logger(__name__)


class Plugin:
    id: str
    name: str
    help: str
    requires_config: bool = False

    @abstractclassmethod
    def on_message(cls, message: Message, channel_config: Optional[Dict] = None):
        pass


@lru_cache
def get_available_plugins():
    """Retrieves every available plugin"""
    plugins = {}
    for ep in pkg_resources.iter_entry_points("butterrobot.plugins"):
        try:
            plugin_cls = ep.load()
            plugins[plugin_cls.id] = plugin_cls
        except Exception as error:
            logger.error(
                "Error loading plugin",
                exception=str(error),
                traceback=traceback.format_exc(),
                plugin=ep.name,
                project_name=ep.dist.project_name,
                entry_point=ep,
                module=ep.module_name,
            )

    return plugins
