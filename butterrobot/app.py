import asyncio
import traceback

from quart import Quart, request
import structlog

import butterrobot.logging  # noqa
from butterrobot.config import ENABLED_PLUGINS
from butterrobot.objects import Message
from butterrobot.plugins import get_available_plugins
from butterrobot.platforms import PLATFORMS
from butterrobot.platforms.base import Platform


logger = structlog.get_logger(__name__)
app = Quart(__name__)
available_platforms = {}
plugins = get_available_plugins()
enabled_plugins = [
    plugin for plugin_name, plugin in plugins.items() if plugin_name in ENABLED_PLUGINS
]


async def handle_message(platform: str, message: Message):
    for plugin in enabled_plugins:
        async for response_message in plugin.on_message(message):
            asyncio.ensure_future(available_platforms[platform].methods.send_message(response_message))


@app.before_serving
async def init_platforms():
    for platform in PLATFORMS.values():
        logger.debug("Setting up", platform=platform.ID)
        try:
            await platform.init(app=app)
            available_platforms[platform.ID] = platform
            logger.info("platform setup completed", platform=platform.ID)
        except platform.PlatformInitError as error:
            logger.error("Platform init error", error=error, platform=platform.ID)


@app.route("/<platform>/incoming", methods=["POST"])
@app.route("/<platform>/incoming/<path:path>", methods=["POST"])
async def incoming_platform_message_view(platform, path=None):
    if platform not in available_platforms:
        return {"error": "Unknown platform"}, 400

    try:
        message = await available_platforms[platform].parse_incoming_message(
            request=request
        )
    except Platform.PlatformAuthResponse as response:
        return response.data, response.status_code
    except Exception as error:
        logger.error(
            "Error parsing message",
            platform=platform,
            error=error,
            traceback=traceback.format_exc(),
        )
        return {"error": str(error)}, 400

    if not message or message.from_bot:
        return {}

    asyncio.ensure_future(handle_message(platform, message))

    return {}


@app.route("/healthz")
def healthz():
    return {}
