#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linguistic Tag Viewer

@author: Hrishikesh Terdalkar
"""

###############################################################################

import datetime
from hashlib import md5

from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_admin import Admin, helpers as admin_helpers


from sqlalchemy import or_, and_, func

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_wtf import CSRFProtect

# local
from models import (db, User)
from models_admin import (SecureAdminIndexView, UserModelView,)

import settings
from reverseproxied import ReverseProxied

###############################################################################
# Import Data

def import_data():
    """Import Data into SQLite3 Database from CSV"""
    # Load CSV files from settings.DATA_DIR
    data_file = []

    with open(data_file, encoding="utf-8") as f:
        rows = [
            line.split(",", 1) for line in f.read().split("\n") if line.strip()
        ]

    objects = []
    # objects = [Sentence(headword=row[0], text=row[1]) for row in rows]
    db.session.add_all(objects)
    db.session.flush()
    db.session.commit()


###############################################################################

webapp = Flask(settings.APP_NAME, static_folder=settings.STATIC_DIR)
webapp.wsgi_app = ReverseProxied(webapp.wsgi_app)
webapp.url_map.strict_slashes = False

webapp.config['SECRET_KEY'] = settings.SECRET_KEY
webapp.config['JSON_AS_ASCII'] = False
webapp.config['JSON_SORT_KEYS'] = False

# SQLAlchemy Config
webapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
webapp.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
webapp.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
}

# Flask Admin Theme
webapp.config["FLASK_ADMIN_SWATCH"] = "united"

# CSRF Token Expiry
webapp.config['WTF_CSRF_TIME_LIMIT'] = None

# Custom
webapp.config["HASH_SALT"] = settings.HASH_SALT

###############################################################################
# Initialize standard Flask extensions

db.init_app(webapp)

# flask-login
login_manager = LoginManager()
login_manager.init_app(webapp)

csrf = CSRFProtect(webapp)
limiter = Limiter(
    key_func=get_remote_address,
    app=webapp,
    default_limits=["1800 per hour"],
    storage_uri="memory://",
)

# flask-admin
admin = Admin(
    webapp,
    name=settings.APP_HEADER,
    index_view=SecureAdminIndexView(name="Database",),
    template_mode="bootstrap4",
    base_template="admin_base.html",
)

admin.add_view(UserModelView(User, db.session))
# admin.add_view(LabelModelView(NodeLabel, db.session, category="Ontology"))

###############################################################################


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"))


###############################################################################


def user_exists(username):
    return User.query.filter_by(username=username).one_or_none() is not None


def validate_user(username, password):
    return User.query.filter_by(
        username=username, hash=compute_user_hash(username, password)
    ).one_or_none()


def compute_user_hash(username, password):
    salt = webapp.config["HASH_SALT"]
    user_md5 = md5(f"{salt}.{username}.{password}".encode())
    return user_md5.hexdigest()


def create_user(username, password):
    user_hash = compute_user_hash(username, password)
    if not user_exists(username):
        user = User(username=username, hash=user_hash)
        db.session.add(user)
        db.session.commit()
        return user


###############################################################################


@webapp.before_first_request
def init_database():
    """Initiate database and create admin user"""
    db.create_all()
    for admin_username, admin_password in settings.ADMIN_USERS.items():
        create_user(admin_username, admin_password)

    # if not Sentence.query.count():
    #     import_data()

    # if not Label.query.count():
    #     db.session.add_all(
    #         [Label(short=k, label=v) for k, v in config.DEFAULT_LABELS.items()]
    #     )
    #     db.session.commit()

###############################################################################


@webapp.context_processor
def insert_global_context():
    return {
        "now": datetime.datetime.now(),
        "title": settings.APP_TITLE,
        "header": settings.APP_HEADER,
        "navigation_menu": settings.NAVIGATION
    }


###############################################################################


@webapp.route("/login", methods=["GET", "POST"])
def show_login():
    if current_user.is_authenticated:
        return redirect(url_for("show_home"))

    data = {}
    data["mode"] = "login"
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if user_exists(username):
            user = validate_user(username, password)
            if user is not None:
                login_user(user)
                flash("Logged in successfully.", "success")
                return redirect(url_for("show_home"))
            else:
                flash("Login failed.", "danger")
        else:
            flash("User does not exist.")
            return redirect(url_for("login"))
    return render_template("login.html", data=data)


@webapp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# --------------------------------------------------------------------------- #

@webapp.route("/terms")
def show_terms():
    data = {'title': 'Terms of Use'}
    return render_template('terms.html', data=data)


@webapp.route("/contact")
def show_contact():
    data = {'title': 'Contact Us'}
    contacts = []
    replacement = {'@': 'at', '.': 'dot'}
    for _contact in settings.CONTACTS:
        contact = _contact.copy()
        email = (
            _contact['email'].replace('.', ' . ').replace('@', ' @ ').split()
        )
        contact['email'] = []

        for email_part in email:
            contact['email'].append({
                'text': replacement.get(email_part, email_part),
                'is_text': replacement.get(email_part) is None
            })
        contacts.append(contact)
    data['contacts'] = contacts
    data['feedback_url'] = settings.FEEDBACK_URL
    return render_template('contact.html', data=data)

# --------------------------------------------------------------------------- #


@webapp.route("/")
def show_home():
    return render_template("about.html")


@webapp.route("/list/")
def show_tag_list():
    return render_template("list.html")


@webapp.route("/tag/")
def show_one_tag():
    return render_template("tag.html")


@webapp.route("/compare/")
def show_compare_tag():
    return render_template("compare.html")


###############################################################################

if __name__ == "__main__":
    import argparse
    import socket

    hostname = socket.gethostname()
    default_host = socket.gethostbyname(hostname)
    default_port = '5000'

    parser = argparse.ArgumentParser(
        description=f"{settings.APP_NAME} Server"
    )
    parser.add_argument(
        "-H", "--host", help="Hostname", default=default_host
    )
    parser.add_argument(
        "-P", "--port", help="Port", default=default_port
    )
    args = vars(parser.parse_args())

    host = args["host"]
    port = args["port"]

    webapp.run(host=host, port=port, debug=True)
