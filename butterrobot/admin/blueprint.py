import os.path

from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from butterrobot.db import User
from butterrobot.plugins import get_available_plugins


admin = Blueprint('admin', __name__, url_prefix='/admin')
admin.template_folder = os.path.join(os.path.dirname(__name__), "templates")

@admin.route("/")
def index_view():
    if not session.get("logged_in", False):
        return redirect(url_for("admin.login_view"))
    return render_template("index.j2")


@admin.route("/login", methods=["GET", "POST"])
def login_view():
    error = None
    if request.method == 'POST':
        user = User.check_credentials(request.form["username"], request.form["password"])
        if not user:
            error = "Incorrect credentials"
        else:
            session['logged_in'] = True
            session["user"] = user
            flash('You were logged in')
            return redirect(url_for('admin.index_view'))
    return render_template("login.j2", error=error)

@admin.route("/login")
def logout_view():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('admin.index_view'))


@admin.route("/plugins")
def plugin_list_view():
    print(get_available_plugins())
    return render_template("plugin_list.j2", plugins=get_available_plugins().values())
