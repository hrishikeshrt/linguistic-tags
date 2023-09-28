#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample Configuration

@author: Hrishikesh Terdalkar
"""

###############################################################################
# generate a nice key using secrets.token_urlsafe()

APP_NAME = "App-Name Viewer"          # used to reference application in code
APP_TITLE = "App-Title"               # displayed in HTML <title>
APP_HEADER = "App-Header"             # displayed as ".lead" header

APP_SINCE = 2023
APP_COPYRIGHT_TEXT = ""
APP_COPYRIGHT_TEXT = "All rights reserved"

SECRET_KEY = "not-so-secret-key"
DEBUG = False

# --------------------------------------------------------------------------- #

STATIC_DIR = "static/"
DATA_DIR = "data/"
LOG_FILE = "samanvaya.log"

# --------------------------------------------------------------------------- #

NAVIGATION = {
    "about": ("show_home", "About"),
    "list": ("show_tag_list", "List"),
    "tag": ("show_one_tag", "Tag"),
    "compare": ("show_compare_tag", "Compare"),
}

# --------------------------------------------------------------------------- #
# list of administrators

ADMIN_USERS = {
    "admin": "admin",
}

# team
TEAM = [
    {
        "name": "Administrator",
        "designation": "Administrator",
        "affiliation": "Earth"
    },
]

# contacts
CONTACTS = [
    {
        "name": "Administrator",
        "email": "admin@localhost",
        "designation": "Administrator",
        "affiliation": "Earth",
    },
]

FEEDBACK_URL = ""

# --------------------------------------------------------------------------- #
# default classification labels

DEFAULT_LABELS = {
    "label-key": "label-name-display",
}

# --------------------------------------------------------------------------- #
# Database

# SQLAlchemy compatible database-uri
DATABASE_URI = "sqlite:///db/main.db"

###############################################################################
