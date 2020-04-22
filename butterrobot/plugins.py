import traceback
import pkg_resources
from abc import abstractclassmethod

import structlog


logger = structlog.get_logger(__name__)


class Plugin:
    @abstractclassmethod
    def on_message(cls, message):
        pass


def get_available_plugins():
    """Retrieves every available plugin"""
    plugins = {}
    logger.debug("Loading plugins")
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

    logger.info(f"Plugins loaded", plugins=list(plugins.keys()))
    return plugins
