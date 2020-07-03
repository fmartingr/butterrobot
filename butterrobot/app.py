import asyncio
import traceback
import urllib.parse

from quart import Quart, request
import structlog

import butterrobot.logging
from butterrobot.config import SLACK_TOKEN, LOG_LEVEL, ENABLED_PLUGINS
from butterrobot.plugins import get_available_plugins
from butterrobot.platforms import PLATFORMS
from butterrobot.platforms.base import Platform


logger = structlog.get_logger(__name__)
app = Quart(__name__)
available_platforms = {}
plugins = get_available_plugins()
enabled_plugins = [plugin for plugin_name, plugin in plugins.items() if plugin_name in ENABLED_PLUGINS]


@app.before_serving
async def init_platforms():
    for platform in PLATFORMS.values():
        logger.debug("Setting up", platform=platform.ID)
        try:
            await platform.init(app=app)
            available_platforms[platform.ID] = platform
            logger.info("platform setup completed", platform=platform.ID)
        except platform.platformInitError as error:
            logger.error(f"platform init error", error=error, platform=platform.ID)


@app.route("/<platform>/incoming", methods=["POST"])
@app.route("/<platform>/incoming/<path:path>", methods=["POST"])
async def incoming_platform_message_view(platform, path=None):
    if platform not in available_platforms:
        return {"error": "Unknown platform"}, 400

    try:
        message = await available_platforms[platform].parse_incoming_message(request=request)
    except Platform.PlatformAuthResponse as response:
        return response.data, response.status_code
    except Exception as error:
        logger.error(f"Error parsing message", platform=platform, error=error, traceback=traceback.format_exc())
        return {"error": str(error)}, 400

    if not message:
        return {}

    for plugin in enabled_plugins:
        if result := await plugin.on_message(message):
            await available_platforms[platform].methods.send_message(result)

    return {}


@app.route("/healthz")
def healthz():
    return {}
