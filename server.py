#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linguistic Tag Viewer

@author: Hrishikesh Terdalkar
"""

###############################################################################

import os
import csv
import logging
import datetime

from flask import (Flask, render_template, redirect, jsonify, url_for,
                   request, flash, session, Response, abort)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_admin import Admin, helpers as admin_helpers

from sqlalchemy import or_, and_, func
from werkzeug.security import check_password_hash

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_wtf import CSRFProtect

# local
from models import (
    db, User, Language,
    SentenceTypeMeaningTag, SentenceTypeMeaningData,
    SentenceTypeStructureTag, SentenceTypeStructureData,
    VoiceTag, VoiceData,
    PartsOfSpeechTag, PartsOfSpeechData,
    VerbalTag, VerbalData,
    TenseAspectMoodTag, TenseAspectMoodData,
    DependencyTag, DependencyData,
    VerbalRootTypeTag, VerbalRootTypeData,
    TAG_LIST, TAG_SCHEMA
)
from models_admin import (
    SecureAdminIndexView, UserModelView, LanguageModelView,
    TagModelView, DataModelView
)

import settings
from utils.reverseproxied import ReverseProxied
from utils.database import create_user, model_to_dict

###############################################################################

logging.basicConfig(format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[logging.FileHandler(settings.LOG_FILE),
                              logging.StreamHandler()])

###############################################################################

webapp = Flask(settings.APP_NAME, static_folder=settings.STATIC_DIR)
webapp.wsgi_app = ReverseProxied(webapp.wsgi_app)
webapp.url_map.strict_slashes = False

webapp.config['SECRET_KEY'] = settings.SECRET_KEY
webapp.config['JSON_AS_ASCII'] = False
webapp.config['JSON_SORT_KEYS'] = False
webapp.config['DEBUG'] = settings.DEBUG

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
admin.add_view(LanguageModelView(Language, db.session))

admin.add_view(TagModelView(SentenceTypeMeaningTag, db.session, category="Tags"))
admin.add_view(TagModelView(SentenceTypeStructureTag, db.session, category="Tags"))
admin.add_view(TagModelView(VoiceTag, db.session, category="Tags"))
admin.add_view(TagModelView(PartsOfSpeechTag, db.session, category="Tags"))
admin.add_view(TagModelView(VerbalTag, db.session, category="Tags"))
admin.add_view(TagModelView(TenseAspectMoodTag, db.session, category="Tags"))
admin.add_view(TagModelView(DependencyTag, db.session, category="Tags"))
admin.add_view(TagModelView(VerbalRootTypeTag, db.session, category="Tags"))

admin.add_view(DataModelView(SentenceTypeMeaningData, db.session, category="Examples"))
admin.add_view(DataModelView(SentenceTypeStructureData, db.session, category="Examples"))
admin.add_view(DataModelView(VoiceData, db.session, category="Examples"))
admin.add_view(DataModelView(PartsOfSpeechData, db.session, category="Examples"))
admin.add_view(DataModelView(VerbalData, db.session, category="Examples"))
admin.add_view(DataModelView(TenseAspectMoodData, db.session, category="Examples"))
admin.add_view(DataModelView(DependencyData, db.session, category="Examples"))
admin.add_view(DataModelView(VerbalRootTypeData, db.session, category="Examples"))

###############################################################################


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("show_login"))


###############################################################################
# Initiate Database


# @webapp.before_first_request
# def init_database():
with webapp.app_context():
    db.create_all()
    for user in settings.USERS:
        create_user(user["username"], user["password"], user["role"])

    data_tables = [
        Language,
        SentenceTypeMeaningTag, SentenceTypeMeaningData,
        SentenceTypeStructureTag, SentenceTypeStructureData,
        VoiceTag, VoiceData,
        PartsOfSpeechTag, PartsOfSpeechData,
        VerbalTag, VerbalData,
        TenseAspectMoodTag, TenseAspectMoodData,
        DependencyTag, DependencyData,
        VerbalRootTypeTag, VerbalRootTypeData,
    ]

    for data_table_model in data_tables:
        if data_table_model.query.count():
            continue

        table_filename = f"{data_table_model.__tablename__}.csv"
        table_filepath = os.path.join(settings.DATA_DIR, table_filename)

        if os.path.isfile(table_filepath):
            with open(table_filepath, encoding="utf-8") as f:
                data = list(csv.DictReader(f))

            db.session.add_all(
                [data_table_model(**row) for row in data]
            )
        db.session.commit()


###############################################################################


@webapp.context_processor
def insert_global_context():
    return {
        "now": datetime.datetime.now(),
        "title": settings.APP_TITLE,
        "header": settings.APP_HEADER,
        "since": settings.APP_SINCE,
        "copyright": settings.APP_COPYRIGHT,
        "navigation_menu": settings.NAVIGATION,
        "footer_links": settings.FOOTER_LINKS,
    }


###############################################################################
# API


@webapp.route("/api/list/languages", methods=["GET"])
def list_languages():
    response = {
        language.id: model_to_dict(language)
        for language in Language.query.all()
    }
    return jsonify(response)


@webapp.route("/api/list/tags", methods=["GET"])
def list_tags():
    response = [
        {
            "category": tag_category,
            "hindi": _hindi,
            "english": _english,
            "count": _model_tag.query.count() if _model_tag is not None else 0
        }
        for tag_category, (_hindi, _english, _model_tag, _model_data) in TAG_LIST.items()
    ]
    return jsonify(response)


@webapp.route("/api/list/<string:tag_category>", methods=["GET"])
@login_required
def list_category_tags(tag_category: str):
    name_hindi, name_english, model_tag, model_data = TAG_LIST[tag_category]
    response = {
        model.id: model_to_dict(model)
        for model in model_tag.query.all()
    }
    return jsonify(response)


@webapp.route("/api/get/<string:tag_category>/<string:tag_ids>", methods=["GET"])
@login_required
def get_category_tags(tag_category: str, tag_ids: str = None):
    name_hindi, name_english, model_tag, model_data = TAG_LIST[tag_category]
    tag_ids = tag_ids.split(",")[:4]
    tags = model_tag.query.filter(model_tag.id.in_(tag_ids)).all()
    if tags is None:
        return jsonify({})

    response = {
        "languages": {
            language.id: model_to_dict(language)
            for language in Language.query.all()
        },
        "schema": TAG_SCHEMA[tag_category],
        "tags": {
            tag.id: {
                "tag": model_to_dict(tag),
                "data": [
                    model_to_dict(row)
                    for row in model_data.query.filter(
                        model_data.tag_id == tag.id
                    ).all()
                ]
            }
            for tag in tags
        }
    }
    return jsonify(response)


###############################################################################


@webapp.route("/login", methods=["GET", "POST"])
def show_login():
    if current_user.is_authenticated:
        flash("Already logged in.")
        return redirect(url_for("show_home"))

    data = {"title": "Login"}
    data["mode"] = "login"
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).one_or_none()
        if user is not None:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Logged in successfully.", "success")
                return redirect(
                    request.args.get("next") or url_for("show_home")
                )
            else:
                flash("Login failed.", "danger")
        else:
            flash("User does not exist.")

    return render_template("login.html", data=data)


@webapp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("show_home"))


# --------------------------------------------------------------------------- #

@webapp.route("/terms")
def show_terms():
    data = {'title': 'Terms of Use'}
    return render_template('terms.html', data=data)


@webapp.route("/team")
def show_team():
    data = {'title': 'Team'}
    data['team'] = settings.TEAM
    return render_template('team.html', data=data)


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
    data = {"title": "About"}
    return render_template("about.html", data=data)


@webapp.route("/tag/")
@login_required
def show_tag():
    data = {"title": "Tag Information"}

    default_category = SentenceTypeMeaningTag.__tablename__
    default_tag_ids = [1]

    data["default_category"] = request.args.get("category", default_category)
    data["default_tag_ids"] = default_tag_ids
    data["max_select"] = settings.MAX_SELECT

    return render_template("tag.html", data=data)


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
