#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask-Admin Models

@author: Hrishikesh Terdalkar
"""

from flask import request, flash, redirect, url_for
from flask_login import current_user

from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

import settings

###############################################################################


class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return (
            current_user.is_authenticated
            and current_user.username in settings.ADMIN_USERS
        )

    def inaccessible_callback(self, name, **kwargs):
        flash("You do not have permission to view this resource.", "error")
        return redirect(url_for('show_login', next=request.url))


class SecureModelView(ModelView):
    def is_accessible(self):
        return (
            current_user.is_authenticated
            and current_user.username in settings.ADMIN_USERS
        )

    def inaccessible_callback(self, name, **kwargs):
        flash("You do not have permission to view this resource.", "error")
        return redirect(url_for("show_login"))

###############################################################################


class BaseModelView(SecureModelView):
    column_display_pk = True
    column_hide_backrefs = False

    can_export = True
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True

    create_modal = True
    edit_modal = True

    can_set_page_size = True

    def __init__(self, model, session, **kwargs):
        if self.form_excluded_columns:
            self.form_excluded_columns = list(self.form_excluded_columns)
        else:
            self.form_excluded_columns = []

        # if columns were excluded from the list view
        # exclude them from create / edit forms as well
        if self.column_exclude_list:
            for field in self.column_exclude_list:
                self.form_excluded_columns.append(field)

        # exclude relationships from showing up in the create / edit forms
        for relationship in model.__mapper__.relationships:
            self.form_excluded_columns.append(relationship.key)

        self.form_excluded_columns = tuple(self.form_excluded_columns)
        super().__init__(model, session, **kwargs)


###############################################################################


class UserModelView(BaseModelView):
    column_exclude_list = ('hash',)
    column_searchable_list = ('username',)


###############################################################################


class BaseMetaModelView(BaseModelView):
    pass


class BaseDataModelView(BaseModelView):
    pass


###############################################################################
