import asyncio

import structlog
from flask import Flask, request

import butterrobot.logging  # noqa
from butterrobot.http import ExternalProxyFix
from butterrobot.queue import q
from butterrobot.config import SECRET_KEY
from butterrobot.platforms import get_available_platforms
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
