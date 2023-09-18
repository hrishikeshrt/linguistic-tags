#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linguistic Tag Viewer

@author: Hrishikesh Terdalkar
"""

###############################################################################

from flask import Flask, render_template

###############################################################################

webapp = Flask("Linguistic Tag Viewer")

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
    webapp.run(debug=True)