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
from butterrobot.plugins import get_available_plugins
from butterrobot.platforms import PLATFORMS, get_available_platforms
from butterrobot.platforms.base import Platform
from butterrobot.admin.blueprint import admin as admin_bp


class ExternalProxyFix(object):
    """
    Custom proxy helper to get the external hostname from the `X-External-Host` header
    used by one of the reverse proxies in front of this in production.
    It does nothing if the header is not present.
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        host = environ.get("HTTP_X_EXTERNAL_HOST", "")
        if host:
            environ["HTTP_HOST"] = host
        return self.app(environ, start_response)


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
