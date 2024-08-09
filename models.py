#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Models

@author: Hrishikesh Terdalkar
"""

###############################################################################

import sqlite3
from datetime import datetime as dt

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum,
    event
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.engine import Engine

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from constants import ROLE_ADMIN, ROLE_CURATOR, ROLE_USER
from constants import ACTION_CREATE, ACTION_EDIT, ACTION_DELETE
from constants import SUGGEST_GENERIC, SUGGEST_CREATE, SUGGEST_EDIT, SUGGEST_DELETE

###############################################################################
# Foreign Key Support for SQLite3


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:
        # play well with other database backends
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


###############################################################################
# Create database connection object

db = SQLAlchemy()

###############################################################################
# Database Models


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    # hash of password
    password = Column(String(255), nullable=False)
    role = Column(
        Enum(ROLE_USER, ROLE_CURATOR, ROLE_ADMIN),
        default=ROLE_USER,
        nullable=False
    )
    is_deleted = Column(Boolean, default=False, nullable=False)

    def __str__(self):
        class_name = self.__class__.__qualname__
        return f"<{class_name} {self.id}: {self.username}>"


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, old_value, initiator):
    if value != old_value:
        return generate_password_hash(value)
    return value

###############################################################################


class Language(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    def __str__(self):
        class_name = self.__class__.__qualname__
        return f"<{class_name} {self.id}: {self.code}>"

###############################################################################
# Comment


class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(f'{User.__tablename__}.id'), nullable=False)
    tablename = Column(String(255), nullable=False)
    action = Column(
        Enum(SUGGEST_GENERIC, SUGGEST_CREATE, SUGGEST_EDIT, SUGGEST_DELETE),
        nullable=False
    )
    comment = Column(Text)
    detail = Column(Text)
    timestamp = Column(DateTime, default=dt.utcnow)

    user = relationship(User.__qualname__, backref=backref('comments'))


###############################################################################
# Change Log


class ChangeLog(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(f'{User.__tablename__}.id'), nullable=False)
    tablename = Column(String(255), nullable=False)
    action = Column(Enum(ACTION_CREATE, ACTION_EDIT, ACTION_DELETE), nullable=False)
    detail = Column(Text)
    timestamp = Column(DateTime, default=dt.utcnow)

    user = relationship(User.__qualname__, backref=backref('changes'))


###############################################################################


class BaseTag(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    description = Column(Text)
    is_deleted = Column(Boolean, default=False, nullable=False)

    def __str__(self):
        class_name = self.__class__.__qualname__
        return f"<{class_name} {self.id}: {self.code}: {self.tag}>"


class BaseData(db.Model):
    __abstract__ = True
    # __related_table__ = None

    id = Column(Integer, primary_key=True)

    # tag_id = Column(Integer, ForeignKey(f'{__related_table__.__tablename__}.id'), nullable=False)
    # language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    explanation = Column(Text)
    is_deleted = Column(Boolean, default=False, nullable=False)

    # language = relationship(Language.__qualname__, backref=backref(f'{__related_table__.__tablename__}_data'))
    # tag = relationship(__related_table__.__qualname__, backref=backref('data'))


###############################################################################


class SentenceMeaningTag(BaseTag):
    pass


class SentenceMeaningData(BaseData):
    tag_id = Column(Integer, ForeignKey(f'{SentenceMeaningTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{SentenceMeaningTag.__tablename__}_data'))
    tag = relationship(SentenceMeaningTag.__qualname__, backref=backref('data'))


###############################################################################


class SentenceStructureTag(BaseTag):
    pass


class SentenceStructureData(BaseData):
    tag_id = Column(Integer, ForeignKey(f'{SentenceStructureTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{SentenceStructureTag.__tablename__}_data'))
    tag = relationship(SentenceStructureTag.__qualname__, backref=backref('data'))


###############################################################################


class VoiceTag(BaseTag):
    subject_verb_agreement = Column(Text)


class VoiceData(BaseData):
    tag_id = Column(Integer, ForeignKey(f'{VoiceTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{VoiceTag.__tablename__}_data'))
    tag = relationship(VoiceTag.__qualname__, backref=backref('data'))


###############################################################################


class PartsOfSpeechTag(BaseTag):
    bis_tag = Column(String(255))


class PartsOfSpeechData(BaseData):
    tag_id = Column(Integer, ForeignKey(f'{PartsOfSpeechTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{PartsOfSpeechTag.__tablename__}_data'))
    tag = relationship(PartsOfSpeechTag.__qualname__, backref=backref('data'))


###############################################################################


class MorphologyTag(BaseTag):
    type = Column(String(255))


class MorphologyData(BaseData):
    tag_id = Column(Integer, ForeignKey(f'{MorphologyTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{MorphologyTag.__tablename__}_data'))
    tag = relationship(MorphologyTag.__qualname__, backref=backref('data'))


###############################################################################


class VerbalTag(BaseTag):
    pass


class VerbalData(BaseData):
    tag_id = Column(Integer, ForeignKey(f'{VerbalTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    verbal = Column(String(255))
    case = Column(Text)
    gender_marking = Column(Text)
    is_part_of_tam = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{VerbalTag.__tablename__}_data'))
    tag = relationship(VerbalTag.__qualname__, backref=backref('data'))


###############################################################################


class TenseAspectMoodTag(BaseTag):
    type = Column(String(255))
    sanskrit_lakara = Column(String(255))
    tense_tag = Column(String(255))
    aspect_tag = Column(String(255))
    mood_tag = Column(String(255))


class TenseAspectMoodData(BaseData):
    tag_id = Column(Integer, ForeignKey(f'{TenseAspectMoodTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    pattern = Column(Text)
    gender_marking = Column(Text)
    syntactic_condition = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{TenseAspectMoodTag.__tablename__}_data'))
    tag = relationship(TenseAspectMoodTag.__qualname__, backref=backref('data'))


###############################################################################


class GroupTag(BaseTag):
    pass


class GroupData(BaseData):
    tag_id = Column(Integer, ForeignKey(f'{GroupTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{GroupTag.__tablename__}_data'))
    tag = relationship(GroupTag.__qualname__, backref=backref('data'))


###############################################################################


class DependencyTag(BaseTag):
    existing_tag = Column(String(255))
    intrasentence_relation = Column(String(255))


class DependencyData(BaseData):
    tag_id = Column(Integer, ForeignKey(f'{DependencyTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    accuracy = Column(Text)
    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{DependencyTag.__tablename__}_data'))
    tag = relationship(DependencyTag.__qualname__, backref=backref('data'))


class DependencyGraphData(db.Model):
    id = Column(Integer, primary_key=True)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    sentence = Column(Text)
    graph = Column(Text)
    comment = Column(Text)

    is_deleted = Column(Boolean, default=False, nullable=False)

    language = relationship(Language.__qualname__, backref=backref(f'dependency_graph_data'))

###############################################################################


class VerbalRootTag(BaseTag):
    pass


class VerbalRootData(BaseData):
    tag_id = Column(Integer, ForeignKey(f'{VerbalRootTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    markers = Column(Text)
    syntactic_condition = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{VerbalRootTag.__tablename__}_data'))
    tag = relationship(VerbalRootTag.__qualname__, backref=backref('data'))


###############################################################################
# Tag Information


class TagInformation(db.Model):
    id = Column(Integer, primary_key=True)
    tablename = Column(
        Enum(
            SentenceMeaningTag.__tablename__,
            SentenceStructureTag.__tablename__,
            VoiceTag.__tablename__,
            GroupTag.__tablename__,
            DependencyTag.__tablename__,
            PartsOfSpeechTag.__tablename__,
            MorphologyTag.__tablename__,
            VerbalTag.__tablename__,
            TenseAspectMoodTag.__tablename__,
            VerbalRootTag.__tablename__,
        ),
        nullable=False
    )
    name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    level = Column(String(255), nullable=False)
    is_visible = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)


###############################################################################

TAG_MODEL_MAP = {
    SentenceMeaningTag.__tablename__: (SentenceMeaningTag, SentenceMeaningData),
    SentenceStructureTag.__tablename__: (SentenceStructureTag, SentenceStructureData),
    VoiceTag.__tablename__: (VoiceTag, VoiceData),
    GroupTag.__tablename__: (GroupTag, GroupData),
    DependencyTag.__tablename__: (DependencyTag, DependencyData),
    PartsOfSpeechTag.__tablename__: (PartsOfSpeechTag, PartsOfSpeechData),
    MorphologyTag.__tablename__: (MorphologyTag, MorphologyData),
    VerbalTag.__tablename__: (VerbalTag, VerbalData),
    TenseAspectMoodTag.__tablename__: (TenseAspectMoodTag, TenseAspectMoodData),
    VerbalRootTag.__tablename__: (VerbalRootTag, VerbalRootData),
}

GRAPH_MODEL_MAP = {
    "dependency_graph": DependencyGraphData
}

TAG_SCHEMA = {
    SentenceMeaningTag.__tablename__: {
        "meta": {},
        "data": {
            "iso_transliteration": "ISO Transliteration",
        },
    },
    SentenceStructureTag.__tablename__: {
        "meta": {},
        "data": {
            "iso_transliteration": "ISO Transliteration",
        }
    },
    VoiceTag.__tablename__: {
        "meta": {},
        "data": {
            "iso_transliteration": "ISO Transliteration",
        },
    },
    PartsOfSpeechTag.__tablename__: {
        "meta": {
            "bis_tag": "BIS Annotation"
        },
        "data": {
            "iso_transliteration": "ISO Transliteration",
        },
    },
    MorphologyTag.__tablename__: {
        "meta": {},
        "data": {
            "iso_transliteration": "ISO Transliteration",
        },
    },
    VerbalTag.__tablename__: {
        "meta": {},
        "data": {
            "verbal": "Kṛt Pratyaya",
            "iso_transliteration": "ISO Transliteration",
            "is_part_of_tam": "Part of TAM Tags?"
        },
    },
    TenseAspectMoodTag.__tablename__: {
        "meta": {
            "tag": "TAM Tag",
            "sanskrit_lakara": "Sanskrit Lakāra",
            "tense_tag": "Tense Tag (K)",
            "aspect_tag": "Aspect Tag (P)",
            "mood_tag": "Mood Tag (V)",
        },
        "data": {
            "iso_transliteration": "ISO Transliteration",
        }
    },
    GroupTag.__tablename__: {
        "meta": {},
        "data": {
            "iso_transliteration": "ISO Transliteration",
        }
    },
    DependencyTag.__tablename__: {
        "meta": {},
        "data": {
            "iso_transliteration": "ISO Transliteration",
        },
    },
    VerbalRootTag.__tablename__: {
        "meta": {},
        "data": {
            "iso_transliteration": "ISO Transliteration",
        },
    },
}

###############################################################################
