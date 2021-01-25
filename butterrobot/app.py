import asyncio
import traceback
from dataclasses import asdict
from functools import lru_cache

from flask import Flask, request, jsonify
import structlog

import butterrobot.logging  # noqa
from butterrobot.queue import q
from butterrobot.db import ChannelQuery
from butterrobot.config import SECRET_KEY, HOSTNAME
from butterrobot.objects import Message, Channel
from butterrobot.http import ExternalProxyFix
from butterrobot.plugins import get_available_plugins
from butterrobot.platforms import PLATFORMS, get_available_platforms
from butterrobot.platforms.base import Platform
from butterrobot.admin.blueprint import admin as admin_bp


loop = asyncio.get_event_loop()
logger = structlog.get_logger(__name__)
app = Flask(__name__)
app.config.update(SECRET_KEY=SECRET_KEY)
app.register_blueprint(admin_bp)
app.wsgi_app = ExternalProxyFix(app.wsgi_app)


@app.route("/<platform>/incoming", methods=["POST"])
@app.route("/<platform>/incoming/<path:path>", methods=["POST"])
def incoming_platform_message_view(platform, path=None):
    if platform not in get_available_platforms():
        return {"error": "Unknown platform"}, 400

    q.put(
        {
            "platform": platform,
            "request": {"path": request.path, "json": request.get_json()},
        }
    )

    return {}

@app.route("/healthz")
def healthz():
    return {}
