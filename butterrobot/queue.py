import threading
import traceback
import queue

import structlog

from butterrobot.db import ChannelQuery
from butterrobot.platforms import get_available_platforms
from butterrobot.platforms.base import Platform
from butterrobot.plugins import get_available_plugins

logger = structlog.get_logger(__name__)
q = queue.Queue()


def handle_message(platform: str, request: dict):
    try:
        message = get_available_platforms()[platform].parse_incoming_message(request=request)
    except Platform.PlatformAuthResponse as response:
        return response.data, response.status_code
    except Exception as error:
        logger.error(
            "Error parsing message",
            platform=platform,
            error=error,
            traceback=traceback.format_exc(),
        )
        return

    logger.info("Received request", platform=platform, message=message)

    if not message or message.from_bot:
        return

    try:
        channel = ChannelQuery.get_by_platform(platform, message.chat)
    except ChannelQuery.NotFound:
        # If channel is still not present on the database, create it (defaults to disabled)
        channel = ChannelQuery.create(platform, message.chat, channel_raw=message.channel.channel_raw)

    if not channel.enabled:
        return

    for plugin_id, channel_plugin in channel.plugins.items():
        if not channel.has_enabled_plugin(plugin_id):
            continue

        for response_message in get_available_plugins()[plugin_id].on_message(message, plugin_config=channel_plugin.config):
            get_available_platforms()[platform].methods.send_message(response_message)


def worker_thread():
    while True:
        item = q.get()
        handle_message(item["platform"], item["request"])
        q.task_done()

# turn-on the worker thread
worker = threading.Thread(target=worker_thread, daemon=True).start()
