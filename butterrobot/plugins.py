import traceback
import pkg_resources
from abc import abstractclassmethod
from functools import lru_cache
from typing import Optional, Dict

import structlog

from butterrobot.objects import Message


logger = structlog.get_logger(__name__)


class Plugin:
    """
    Base Plugin class.

    All attributes are required except for `requires_config`.
    """

    id: str
    name: str
    help: str
    requires_config: bool = False

    @abstractclassmethod
    def on_message(cls, message: Message, channel_config: Optional[Dict] = None):
        """
        Function called for each message received on the chat.

        It should exit as soon as possible (usually checking for a keyword or something)
        similar just at the start.

        If the plugin needs to be executed (keyword matches), keep it as fast as possible
        as this currently blocks the execution of the rest of the plugins on the channel
        until this does not finish.
        TODO: Update this once we go proper async plugin/message integration

        In case something needs to be answered to the channel, you can `yield` a `Message`
        instance and it will be relayed using the appropriate provider.
        """
        pass


@lru_cache
def get_available_plugins():
    """
    Retrieves every available auto discovered plugin
    """
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

    logger.info("Plugins loaded", plugins=list(plugins.keys()))
    return plugins
