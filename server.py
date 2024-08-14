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
    db, User, Language, ChangeLog,
    SentenceMeaningTag, SentenceMeaningData,
    SentenceStructureTag, SentenceStructureData,
    VoiceTag, VoiceData,
    PartsOfSpeechTag, PartsOfSpeechData,
    MorphologyTag, MorphologyData,
    VerbalTag, VerbalData,
    TenseAspectMoodTag, TenseAspectMoodData,
    GroupTag, GroupData,
    DependencyTag, DependencyData, DependencyGraphData,
    VerbalRootTag, VerbalRootData,
    TagInformation,
    Comment,
    TAG_MODEL_MAP, TAG_SCHEMA, GRAPH_MODEL_MAP
)
from models_admin import (
    SecureAdminIndexView, UserModelView, LanguageModelView,
    TagInformationModelView,
    TagModelView, DataModelView, GraphModelView,
    ChangeLogModelView,
    CommentModelView,
)

import settings
import constants
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
    template_mode="bootstrap4"
)

admin.add_view(UserModelView(User, db.session))
admin.add_view(LanguageModelView(Language, db.session))
admin.add_view(TagInformationModelView(TagInformation, db.session))

admin.add_view(TagModelView(SentenceMeaningTag, db.session, category="Tags"))
admin.add_view(TagModelView(SentenceStructureTag, db.session, category="Tags"))
admin.add_view(TagModelView(VoiceTag, db.session, category="Tags"))
admin.add_view(TagModelView(PartsOfSpeechTag, db.session, category="Tags"))
admin.add_view(TagModelView(MorphologyTag, db.session, category="Tags"))
admin.add_view(TagModelView(VerbalTag, db.session, category="Tags"))
admin.add_view(TagModelView(TenseAspectMoodTag, db.session, category="Tags"))
admin.add_view(TagModelView(GroupTag, db.session, category="Tags"))
admin.add_view(TagModelView(DependencyTag, db.session, category="Tags"))
admin.add_view(TagModelView(VerbalRootTag, db.session, category="Tags"))

admin.add_view(DataModelView(SentenceMeaningData, db.session, category="Examples"))
admin.add_view(DataModelView(SentenceStructureData, db.session, category="Examples"))
admin.add_view(DataModelView(VoiceData, db.session, category="Examples"))
admin.add_view(DataModelView(PartsOfSpeechData, db.session, category="Examples"))
admin.add_view(DataModelView(MorphologyData, db.session, category="Examples"))
admin.add_view(DataModelView(VerbalData, db.session, category="Examples"))
admin.add_view(DataModelView(TenseAspectMoodData, db.session, category="Examples"))
admin.add_view(DataModelView(GroupData, db.session, category="Examples"))
admin.add_view(DataModelView(DependencyData, db.session, category="Examples"))
admin.add_view(DataModelView(VerbalRootData, db.session, category="Examples"))

admin.add_view(GraphModelView(DependencyGraphData, db.session, category="Graphs"))

admin.add_view(ChangeLogModelView(ChangeLog, db.session))
admin.add_view(CommentModelView(Comment, db.session))

###############################################################################


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({
            "success": False,
            "unauthorized": True,
            "message": "Login required.",
            "style": "warning"
        })
    else:
        flash("Login required.", "warning")
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
        SentenceMeaningTag, SentenceMeaningData,
        SentenceStructureTag, SentenceStructureData,
        VoiceTag, VoiceData,
        PartsOfSpeechTag, PartsOfSpeechData,
        MorphologyTag, MorphologyData,
        VerbalTag, VerbalData,
        TenseAspectMoodTag, TenseAspectMoodData,
        GroupTag, GroupData,
        DependencyTag, DependencyData,
        VerbalRootTag, VerbalRootData,
        TagInformation,
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
        "roles": {
            "ROLE_ADMIN": constants.ROLE_ADMIN,
            "ROLE_CURATOR": constants.ROLE_CURATOR,
            "ROLE_USER": constants.ROLE_USER
        },
        "comment": {
            "actions": constants.SUGGEST_ACTION_TEXT_MAP
        }
    }


###############################################################################
# API


@webapp.route("/api/list/languages", methods=["GET"])
def list_languages():
    response = {
        language.id: model_to_dict(language)
        for language in Language.query.filter(
            Language.is_deleted == False  # noqa
        ).all()
    }
    return jsonify(response)


@webapp.route("/api/list/tags", methods=["GET"])
def list_tags():
    response = []
    for category in TagInformation.query.filter(TagInformation.is_visible == True).all():
        _model_tag, _model_data = TAG_MODEL_MAP[category.tablename]
        response.append({
            "tablename": category.tablename,
            "name": category.name,
            "english_name": category.english_name,
            "level": category.level,
            "count": _model_tag.query.filter(
                _model_tag.is_deleted == False  # noqa
            ).count() if _model_tag is not None else 0
        })

    return jsonify(response)


@webapp.route("/api/list/<string:tag_category>", methods=["GET"])
@login_required
def list_category_tags(tag_category: str):
    model_tag, model_data = TAG_MODEL_MAP[tag_category]
    response = [
        model_to_dict(model)
        for model in model_tag.query.filter(
            model_tag.is_deleted == False  # noqa
        ).order_by(model_tag.code).all()
    ]
    return jsonify(response)


@webapp.route("/api/get/<string:tag_category>/<string:tag_ids>", methods=["GET"])
@login_required
def get_category_tags(tag_category: str, tag_ids: str = None):
    model_tag, model_data = TAG_MODEL_MAP[tag_category]
    tag_ids = tag_ids.split(",")[:4]
    tags = model_tag.query.filter(
        model_tag.id.in_(tag_ids),
        model_tag.is_deleted == False  # noqa
    ).order_by(model_tag.code).all()
    if tags is None:
        return jsonify({})

    response = {
        "languages": {
            language.id: model_to_dict(language)
            for language in Language.query.filter(
                Language.is_deleted == False  # noqa
            ).all()
        },
        "schema": TAG_SCHEMA[tag_category],
        "tags": [
            {
                "tag": model_to_dict(tag),
                "data": [
                    model_to_dict(row)
                    for row in model_data.query.filter(
                        model_data.tag_id == tag.id,
                        model_data.is_deleted == False  # noqa
                    ).all()
                ]
            }
            for tag in tags
        ]
    }
    return jsonify(response)



@webapp.route("/api/graph/get/<string:graph_category>/", methods=["GET"])
@webapp.route("/api/graph/get/<string:graph_category>/<string:language_id>", methods=["GET"])
@login_required
def get_category_graphs(graph_category: str, language_id: int = None):
    model_data = GRAPH_MODEL_MAP[graph_category]
    graphs = model_data.query.filter(
        model_data.is_deleted == False  # noqa
    ).order_by(model_data.group_id, model_data.language_id).all()
    if graphs is None:
        return jsonify({})

    response = {
        "languages": {
            language.id: model_to_dict(language)
            for language in Language.query.filter(
                Language.is_deleted == False  # noqa
            ).all()
        },
        "graphs": [
            {
                "id": graph.id,
                "group_id": graph.group_id,
                "language_id": graph.language_id,
                "sentence": graph.sentence,
                "iso_transliteration": graph.iso_transliteration,
                "gloss": graph.gloss,
                "graph": graph.graph,
                "comment": graph.comment
            }
            for graph in graphs
        ]
    }
    return jsonify(response)


@webapp.route("/api/post/comment", methods=["POST"])
@login_required
def post_comment():
    user_id = current_user.id
    tablename = request.form.get("tablename")
    action = request.form.get("action")
    comment = request.form.get("comment")
    detail = request.form.get("detail")

    response = {"success": False}
    try:
        _comment = Comment()
        _comment.user_id = user_id
        _comment.tablename = tablename
        _comment.action = action
        _comment.comment = comment
        _comment.detail = detail
        db.session.add(_comment)
        db.session.commit()
        response["success"] = True
        response["message"] = "Comment added successfully."
        response["style"] = "success"
    except Exception as e:
        webapp.logger.exception(e)
        response["message"] = "Something went wrong."
        response["style"] = "danger"
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


@webapp.route("/tag/", methods=["GET", "POST"])
@login_required
def show_tag():
    data = {"title": "Tag Information"}

    default_category = SentenceMeaningTag.__tablename__
    default_tag_ids = [1]
    default_tag_ids_str = ",".join(map(str, default_tag_ids))

    data["max_select"] = settings.MAX_SELECT

    if request.method == "POST":
        _category = request.form.get("category", default_category)
        _tag_ids = request.form.get("tag_ids", default_tag_ids_str)
    else:
        _category = request.args.get("category", default_category)
        _tag_ids = request.args.get("tag_ids", default_tag_ids_str)

    data["default_category"] = _category
    data["default_tag_ids"] = list(map(int, _tag_ids.split(",")))

    return render_template("tag.html", data=data)


@webapp.route("/graph/", methods=["GET", "POST"])
@login_required
def show_graph():
    data = {"title": "Graph"}
    default_category = "dependency_graph"
    default_graph_id = 1
    if request.method == "POST":
        _category = request.form.get("category", default_category)
        _graph_id = request.form.get("graph_id", default_graph_id)
    else:
        _category = request.args.get("category", default_category)
        _graph_id = request.args.get("graph_id", default_graph_id)

    data["default_category"] = _category
    data["default_graph_id"] = _graph_id

    return render_template("graph.html", data=data)


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
