#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample Configuration

@author: Hrishikesh Terdalkar
"""

import os
from constants import ROLE_USER, ROLE_CURATOR, ROLE_ADMIN

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

APP_DIR = os.path.dirname(os.path.realpath(__file__))

STATIC_DIR = os.path.join(APP_DIR, "static/")
DATA_DIR = os.path.join(APP_DIR, "data/")
LOG_FILE = os.path.join(APP_DIR, "samanvaya.log")

DATABASE_DIR = os.path.join(APP_DIR, "db/")

# --------------------------------------------------------------------------- #

MAX_SELECT = 3

NAVIGATION = {
    "about": ("show_home", "About"),
    "tag": ("show_tag", "View"),
}

FOOTER_LINKS = {
    "terms": ("show_terms", "Terms"),
    "team": ("show_team", "Team"),
    "contact": ("show_contact", "Contact"),
}

# --------------------------------------------------------------------------- #
# list of administrators

USERS = [
    {
        "username": "admin",
        "password": "admin",
        "role": ROLE_ADMIN
    },
    {
        "username": "user",
        "password": "user",
        "role": ROLE_USER
    },
]

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
DATABASE_URI = f"sqlite:///{os.path.join(DATABASE_DIR, 'main.db')}"

###############################################################################
