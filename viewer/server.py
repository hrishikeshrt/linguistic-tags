#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linguistic Tag Viewer

@author: Hrishikesh Terdalkar
"""

###############################################################################

from flask import Flask, render_template
from sqlalchemy import or_, and_, func

from flask_admin import Admin, helpers as admin_helpers

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_wtf import CSRFProtect

# local
# from models_sqla import (db,)
# from models_admin import (SecureAdminIndexView,)

# from settings import app
from reverseproxied import ReverseProxied

###############################################################################

webapp = Flask("Linguistic Tag Viewer")
webapp.wsgi_app = ReverseProxied(webapp.wsgi_app)
webapp.url_map.strict_slashes = False

# webapp.config['SECRET_KEY'] = app.secret_key
webapp.config['JSON_AS_ASCII'] = False
webapp.config['JSON_SORT_KEYS'] = False

# # SQLAlchemy Config
# webapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# webapp.config['SQLALCHEMY_DATABASE_URI'] = app.sqla['database_uri']
# webapp.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     "pool_pre_ping": True,
# }
# # Flask Admin Theme
# webapp.config["FLASK_ADMIN_SWATCH"] = "united"

# # CSRF Token Expiry
webapp.config['WTF_CSRF_TIME_LIMIT'] = None

###############################################################################
# Initialize standard Flask extensions

# db.init_app(webapp)
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
    name="Linguistic Tag Viewer Admin",
    # index_view=SecureAdminIndexView(
    #     name="Database",
    #     url="/admin/database"
    # ),
    template_mode="bootstrap4",
    # base_template="admin_base.html",
)
# admin.add_view(UserModelView(User, db.session))
# admin.add_view(LabelModelView(NodeLabel, db.session, category="Ontology"))

###############################################################################

NAVIGATION = {
    "home": ("Home", "show_tag_list"),
    "tag": ("Tag", "show_one_tag"),
    "compare": ("Compare", "show_compare_tag"),
}

###############################################################################


@webapp.context_processor
def insert_global_context():
    return {
        "title": "Linguistic Tag Viewer",
        "header": "Linguistic Tag Viewer",
        "navigation": NAVIGATION
    }


###############################################################################


@webapp.route("/")
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

    parser = argparse.ArgumentParser(description="Linguistic Tag Viewer Server")
    parser.add_argument("-H", "--host", help="Hostname", default=default_host)
    parser.add_argument("-P", "--port", help="Port", default=default_port)
    args = vars(parser.parse_args())

    host = args["host"]
    port = args["port"]

    webapp.run(host=host, port=port, debug=True)
