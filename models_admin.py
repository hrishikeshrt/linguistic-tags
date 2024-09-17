#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask-Admin Models

@author: Hrishikesh Terdalkar
"""

import os
import json
import shutil

from sqlalchemy import func

from flask import request, flash, redirect, url_for, current_app
from flask_login import current_user

from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.babel import gettext

from flask_admin.form import FileUploadField
from flask_wtf.file import FileRequired, FileStorage
from werkzeug.utils import secure_filename

from settings import UPLOAD_DIR
from models import ChangeLog
from constants import ROLE_USER, ROLE_CURATOR, ROLE_ADMIN
from constants import ACTION_CREATE, ACTION_EDIT, ACTION_DELETE

###############################################################################

ADMIN_ROLES = [ROLE_CURATOR, ROLE_ADMIN]

###############################################################################


class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return (
            current_user.is_authenticated
            and current_user.role in ADMIN_ROLES
        )

    def inaccessible_callback(self, name, **kwargs):
        flash("You do not have permission to view this resource.", "error")
        return redirect(url_for("show_login", next=request.url))


class SecureModelView(ModelView):
    def is_accessible(self):
        return (
            current_user.is_authenticated
            and current_user.role in ADMIN_ROLES
        )

    def inaccessible_callback(self, name, **kwargs):
        flash("You do not have permission to view this resource.", "error")
        return redirect(url_for("show_login"))


###############################################################################


class ReadOnlyModelView(SecureModelView):
    column_display_pk = True
    can_set_page_size = True

    can_create = False
    can_edit = False
    can_delete = False

    can_export = True
    export_types = ("csv", "tsv", "json", "xlsx")


class AdminOnlyModelView(SecureModelView):
    def is_accessible(self):
        return (
            current_user.is_authenticated and current_user.role == ROLE_ADMIN
        )


###############################################################################


class BaseModelView(SecureModelView):
    column_display_pk = True

    can_export = True
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    create_modal = True
    edit_modal = True
    details_modal = True

    can_set_page_size = True
    export_types = ("csv", "tsv", "json", "xlsx")
    column_exclude_list = ("is_deleted",)
    column_details_exclude_list = ("is_deleted",)

    # custom options
    exclude_relationships = False

    def get_query(self):
        return self.session.query(self.model).filter(self.model.is_deleted == False)  # noqa

    def get_count_query(self):
        return self.session.query(func.count('*')).select_from(self.model).filter(self.model.is_deleted == False)  # noqa

    def delete_model(self, model):
        try:
            self.on_model_delete(model)
            model.is_deleted = True
            self.session.add(model)
            self.session.commit()
            self.after_model_delete(model)
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(
                    gettext(
                        "Failed to delete record. %(error)s", error=str(ex)
                    ),
                    "error"
                )
            self.session.rollback()
            return False
        else:
            self.after_model_delete(model)
        return True

    def on_model_change(self, form, model, is_created):
        detail = {}
        if is_created:
            self.session.flush()

        detail["id"] = model.id
        for field, data in form._fields.items():
            if isinstance(data.data, FileStorage):
                detail[field] = {"filename": data.data.filename}
            elif hasattr(data, "get_pk"):
                old_attr = data.get_pk(data.object_data) if data.object_data else None
                new_attr = data.get_pk(data.data) if data.data else None
            else:
                old_attr = data.object_data
                new_attr = data.data

            if old_attr != new_attr:
                detail[field] = (
                    new_attr
                    if is_created
                    else {"old": old_attr, "new": new_attr}
                )
                if field == "password":
                    detail[field] = True

        change_log = ChangeLog(
            user_id=current_user.id,
            tablename=model.__tablename__,
            action=(ACTION_CREATE if is_created else ACTION_EDIT),
            detail=json.dumps(detail, ensure_ascii=True)
        )
        self.session.add(change_log)
        # commit is performed in parent action

    def on_model_delete(self, model):
        detail = {"id": model.id}
        change_log = ChangeLog(
            user_id=current_user.id,
            tablename=model.__tablename__,
            action=ACTION_DELETE,
            detail=json.dumps(detail)
        )
        self.session.add(change_log)
        # commit is performed in parent action

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
        if self.exclude_relationships:
            for relationship in model.__mapper__.relationships:
                self.form_excluded_columns.append(relationship.key)

        self.form_excluded_columns = tuple(self.form_excluded_columns)
        super().__init__(model, session, **kwargs)


###############################################################################


class BaseAdminModelView(BaseModelView):
    @property
    def can_create(self):
        return (
            current_user.is_authenticated and current_user.role == ROLE_ADMIN
        )

    @property
    def can_edit(self):
        return (
            current_user.is_authenticated and current_user.role == ROLE_ADMIN
        )

    @property
    def can_delete(self):
        return (
            current_user.is_authenticated and current_user.role == ROLE_ADMIN
        )


###############################################################################


class PublicationAdminView(BaseAdminModelView):
    form_extra_fields = {
        "pdf_file": FileUploadField(
            "PDF File",
            # validators=[FileRequired()],
            base_path=UPLOAD_DIR,
            allowed_extensions=["pdf"]
        )
    }

    def on_model_change(self, form, model, is_created):
        # Handle the file upload
        if form.pdf_file.data:
            # Save the new file
            upload_filename = secure_filename(form.pdf_file.data.filename)
            upload_filepath = os.path.join(
                current_app.config['UPLOAD_FOLDER'],
                upload_filename
            )
            form.pdf_file.data.seek(0)
            form.pdf_file.data.save(upload_filepath)
            # print("Size on Disk:", os.path.getsize(upload_filepath))

            if form.filename.data:
                save_filename = secure_filename(form.filename.data)
                if save_filename != upload_filename:
                    save_filepath = os.path.join(
                        current_app.config['UPLOAD_FOLDER'],
                        save_filename
                    )
                    shutil.move(upload_filepath, save_filepath)
                model.filename = save_filename
            else:
                model.filename = upload_filename
        elif form.filename.data:
            filename_old = form.filename.object_data
            filename_new = secure_filename(form.filename.data)
            # Update the filename in the database
            if filename_new != filename_old:
                filepath_old = os.path.join(
                    current_app.config['UPLOAD_FOLDER'],
                    filename_old
                )
                filepath_new = os.path.join(
                    current_app.config['UPLOAD_FOLDER'],
                    filename_new
                )
                # Rename the file on disk
                shutil.move(filepath_old, filepath_new)

        # Call the parent method to handle logging and other operations
        super().on_model_change(form, model, is_created)

###############################################################################


class ChangeLogModelView(ReadOnlyModelView, AdminOnlyModelView):
    column_searchable_list = ("user_id", "action", "detail")


###############################################################################


class CommentModelView(ReadOnlyModelView):
    column_searchable_list = ("user_id", "action", "comment", "detail")


###############################################################################


class UserModelView(BaseAdminModelView, AdminOnlyModelView):
    column_searchable_list = ("username",)

    # custom options
    exclude_relationships = True


class LanguageModelView(BaseAdminModelView):
    column_searchable_list = ("code", "name", "english_name")

    # custom options
    exclude_relationships = True

###############################################################################


class TagInformationModelView(BaseAdminModelView, AdminOnlyModelView):
    can_create = False
    can_delete = False
    can_export = True

    export_types = ("csv", "tsv", "json", "xlsx")

    column_searchable_list = ("tablename", "name", "english_name")


###############################################################################


class TagModelView(BaseModelView):
    column_searchable_list = (
        "code",
        "tag",
        "name",
        "english_name",
        "description"
    )

    # custom options
    exclude_relationships = True


class DataModelView(BaseModelView):
    column_searchable_list = (
        "example",
        "iso_transliteration",
        "sanskrit_translation",
        "english_translation",
    )


class GraphModelView(BaseModelView):
    column_searchable_list = (
        "sentence",
        "graph",
        "comment",
    )

###############################################################################
