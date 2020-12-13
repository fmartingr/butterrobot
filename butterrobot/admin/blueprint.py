import json
import os.path
from functools import wraps

import structlog
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
    g,
)

from butterrobot.config import HOSTNAME
from butterrobot.db import UserQuery, ChannelQuery, ChannelPluginQuery
from butterrobot.plugins import get_available_plugins


admin = Blueprint("admin", __name__, url_prefix="/admin")
admin.template_folder = os.path.join(os.path.dirname(__name__), "templates")
logger = structlog.get_logger(__name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("admin.login_view", next=request.path))
        return f(*args, **kwargs)

    return decorated_function


@admin.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        try:
            user = UserQuery.get(user_id)
            g.user = user
        except UserQuery.NotFound:
            g.user = None


@admin.route("/")
@login_required
def index_view():
    if not session.get("logged_in", False):
        logger.info(url_for("admin.login_view"))
        return redirect(url_for("admin.login_view"))
    return redirect(url_for("admin.channel_list_view"))


@admin.route("/login", methods=["GET", "POST"])
def login_view():
    error = None
    if request.method == "POST":
        user = UserQuery.check_credentials(
            request.form["username"], request.form["password"]
        )
        if not user:
            flash("Incorrect credentials", category="danger")
        else:
            session["logged_in"] = True
            session["user_id"] = user.id
            flash("You were logged in", category="success")
            _next = request.args.get("next", url_for("admin.index_view"))
            return redirect(_next)
    return render_template("login.j2", error=error)


@admin.route("/logout")
@login_required
def logout_view():
    session.clear()
    flash("You were logged out", category="success")
    return redirect(url_for("admin.index_view"))


@admin.route("/plugins")
@login_required
def plugin_list_view():
    return render_template("plugin_list.j2", plugins=get_available_plugins().values())


@admin.route("/channels")
@login_required
def channel_list_view():
    channels = ChannelQuery.all()
    return render_template("channel_list.j2", channels=ChannelQuery.all())


@admin.route("/channels/<channel_id>", methods=["GET", "POST"])
@login_required
def channel_detail_view(channel_id):
    if request.method == "POST":
        ChannelQuery.update(
            channel_id, enabled=request.form["enabled"] == "true",
        )
        flash("Channel updated", "success")

    channel = ChannelQuery.get(channel_id)
    return render_template(
        "channel_detail.j2", channel=channel, plugins=get_available_plugins()
    )


@admin.route("/channel/<channel_id>/delete", methods=["POST"])
@login_required
def channel_delete_view(channel_id):
    ChannelQuery.delete(channel_id)
    flash("Channel removed", category="success")
    return redirect(url_for("admin.channel_list_view"))


@admin.route("/channelplugins", methods=["POST"])
@login_required
def channel_plugin_list_view():
    data = request.form
    try:
        ChannelPluginQuery.create(
            data["channel_id"], data["plugin_id"], enabled=data["enabled"] == "y"
        )
        flash(f"Plugin {data['plugin_id']} added to the channel", "success")
    except ChannelPluginQuery.Duplicated:
        flash(f"Plugin {data['plugin_id']} is already present on the channel", "error")
    return redirect(request.headers.get("Referer"))


@admin.route("/channelplugins/<channel_plugin_id>", methods=["GET", "POST"])
@login_required
def channel_plugin_detail_view(channel_plugin_id):
    if request.method == "POST":
        ChannelPluginQuery.update(
            channel_plugin_id, enabled=request.form["enabled"] == "true",
        )
        flash("Plugin updated", category="success")

    return redirect(request.headers.get("Referer"))


@admin.route("/channelplugins/<channel_plugin_id>/delete", methods=["POST"])
@login_required
def channel_plugin_delete_view(channel_plugin_id):
    ChannelPluginQuery.delete(channel_plugin_id=channel_plugin_id)
    flash("Plugin removed", category="success")
    return redirect(request.headers.get("Referer"))
