#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constants

@author: Hrishikesh Terdalkar
"""

###############################################################################

ROLE_USER = "user"
ROLE_CURATOR = "curator"
ROLE_ADMIN = "admin"

###############################################################################

ACTION_CREATE = "create"
ACTION_EDIT = "edit"
ACTION_DELETE = "delete"

###############################################################################

SUGGEST_GENERIC = "suggest_generic"
SUGGEST_CREATE = "suggest_create"
SUGGEST_EDIT = "suggest_edit"
SUGGEST_DELETE = "suggest_delete"

SUGGEST_GENERIC_TEXT = "Generic"
SUGGEST_CREATE_TEXT = "Create"
SUGGEST_EDIT_TEXT = "Edit"
SUGGEST_DELETE_TEXT = "Delete"

SUGGEST_ACTION_TEXT_MAP = {
    SUGGEST_GENERIC: SUGGEST_GENERIC_TEXT,
    SUGGEST_CREATE: SUGGEST_CREATE_TEXT,
    SUGGEST_EDIT: SUGGEST_EDIT_TEXT,
    SUGGEST_DELETE: SUGGEST_DELETE_TEXT,
}

###############################################################################
