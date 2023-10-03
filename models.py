#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Models

@author: Hrishikesh Terdalkar
"""

###############################################################################

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship, backref

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy, event
from werkzeug.security import generate_password_hash

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
    role = Column(Enum('user', 'admin'), default='user', nullable=False)


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


###############################################################################


class BaseTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)


class BaseData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{BaseTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)

    language = relationship(Language.__qualname__, backref=backref(f'{BaseTag.__tablename__}_data'))
    tag = relationship(BaseTag.__qualname__, backref=backref('data'))

###############################################################################


class SentenceMeaningTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    description = Column(Text)


class SentenceMeaningData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{SentenceMeaningTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{SentenceMeaningTag.__tablename__}_data'))
    tag = relationship(SentenceMeaningTag.__qualname__, backref=backref('data'))


###############################################################################


class SentenceStructureTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    description = Column(Text)


class SentenceStructureData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{SentenceStructureTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{SentenceStructureTag.__tablename__}_data'))
    tag = relationship(SentenceStructureTag.__qualname__, backref=backref('data'))


###############################################################################


class VoiceTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    description = Column(Text)
    subject_verb_agreement = Column(Text)


class VoiceData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{VoiceTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{VoiceTag.__tablename__}_data'))
    tag = relationship(VoiceTag.__qualname__, backref=backref('data'))


###############################################################################


class PartsOfSpeechTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    bis_tag = Column(String(255))
    description = Column(Text)


class PartsOfSpeechData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{PartsOfSpeechTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{PartsOfSpeechTag.__tablename__}_data'))
    tag = relationship(PartsOfSpeechTag.__qualname__, backref=backref('data'))


###############################################################################


class MorphologyTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    type = Column(String(255))
    description = Column(Text)


class MorphologyData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{MorphologyTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{MorphologyTag.__tablename__}_data'))
    tag = relationship(MorphologyTag.__qualname__, backref=backref('data'))


###############################################################################


class VerbalTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    description = Column(Text)


class VerbalData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{VerbalTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    verbal = Column(String(255))
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    case = Column(Text)
    gender_marking = Column(Text)
    is_part_of_tam = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{VerbalTag.__tablename__}_data'))
    tag = relationship(VerbalTag.__qualname__, backref=backref('data'))


###############################################################################


class TenseAspectMoodTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    type = Column(String(255))
    sanskrit_lakara = Column(String(255))
    tense_tag = Column(String(255))
    aspect_tag = Column(String(255))
    mood_tag = Column(String(255))
    description = Column(Text)


class TenseAspectMoodData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{TenseAspectMoodTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    pattern = Column(Text)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    gender_marking = Column(Text)
    syntactic_condition = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{TenseAspectMoodTag.__tablename__}_data'))
    tag = relationship(TenseAspectMoodTag.__qualname__, backref=backref('data'))


###############################################################################


class GroupTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    description = Column(Text)


class GroupData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{GroupTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{GroupTag.__tablename__}_data'))
    tag = relationship(GroupTag.__qualname__, backref=backref('data'))


###############################################################################


class DependencyTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    existing_tag = Column(String(255))
    intrasentence_relation = Column(String(255))
    description = Column(Text)


class DependencyData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{DependencyTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    accuracy = Column(Text)
    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{DependencyTag.__tablename__}_data'))
    tag = relationship(DependencyTag.__qualname__, backref=backref('data'))


###############################################################################


class VerbalRootTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    description = Column(Text)


class VerbalRootData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{VerbalRootTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    explanation = Column(Text)
    markers = Column(Text)
    syntactic_condition = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{VerbalRootTag.__tablename__}_data'))
    tag = relationship(VerbalRootTag.__qualname__, backref=backref('data'))


###############################################################################


TAG_LIST = {
    SentenceMeaningTag.__tablename__: ("अर्थानुसार-वाक्यप्रकार", "Sentence Meaning", "Sentence", SentenceMeaningTag, SentenceMeaningData),
    SentenceStructureTag.__tablename__: ("रचनानुसार-वाक्यप्रकार", "Sentence Structure", "Sentence", SentenceStructureTag, SentenceStructureData),
    VoiceTag.__tablename__: ("क्रिया-वाच्य", "Voice", "Sentence", VoiceTag, VoiceData),
    GroupTag.__tablename__: ("शब्द-समूह", "Group", "Sentence", GroupTag, GroupData),
    DependencyTag.__tablename__: ("आश्रय", "Dependency", "Sentence", DependencyTag, DependencyData),
    PartsOfSpeechTag.__tablename__: ("शब्द-प्रकार", "Parts-of-Speech (POS)", "Word", PartsOfSpeechTag, PartsOfSpeechData),
    MorphologyTag.__tablename__: ("शब्द-रूप", "Morphology", "Word", MorphologyTag, MorphologyData),
    VerbalTag.__tablename__: ("क्रियामूलक-कृद्", "Verbal", "Word", VerbalTag, VerbalData),
    TenseAspectMoodTag.__tablename__: ("क्रिया-कालादि", "Tense-Aspect-Mood (TAM)", "Word", TenseAspectMoodTag, TenseAspectMoodData),
    VerbalRootTag.__tablename__: ("धातुप्रकार", "Verbal Root", "Word", VerbalRootTag, VerbalRootData),
    # "11": ("कर्म-प्रधानता", "Ergativity", None, None)
}

TAG_SCHEMA = {
    SentenceMeaningTag.__tablename__: {
        "meta": {},
        "data": {
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "markers": "Markers"
        },
    },
    SentenceStructureTag.__tablename__: {
        "meta": {},
        "data": {
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "markers": "Markers"
        }
    },
    VoiceTag.__tablename__: {
        "meta": {},
        "data": {
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "markers": "Markers"
        },
    },
    PartsOfSpeechTag.__tablename__: {
        "meta": {
            "bis_tag": "BIS Annotation"
        },
        "data": {
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "markers": "Markers"
        },
    },
    MorphologyTag.__tablename__: {
        "meta": {},
        "data": {
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "markers": "Markers"
        },
    },
    VerbalTag.__tablename__: {
        "meta": {},
        "data": {
            "verbal": "Kṛt Pratyaya",
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "case": "Case",
            "gender_marking": "Gender Marking",
            "is_part_of_tam": "Part of TAM Tags?"
        },
    },
    TenseAspectMoodTag.__tablename__: {
        "meta": {
            "tag": "TAM Tag",
            "name": "Name",
            "english_name": "English Name",
            "type": "Type",
            "sanskrit_lakara": "Sanskrit Lakāra",
            "tense_tag": "Tense Tag (K)",
            "aspect_tag": "Aspect Tag (P)",
            "mood_tag": "Mood Tag (V)",
            "description": "Description",
        },
        "data": {
            "pattern": "Pattern",
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "gender_marking": "Gender Marking",
            "syntactic_condition": "Syntactic Condition",
        }
    },
    GroupTag.__tablename__: {
        "meta": {},
        "data": {
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "markers": "Markers",
        }
    },
    DependencyTag.__tablename__: {
        "meta": {},
        "data": {
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "accuracy": "Accuracy",
            "markers": "Markers",
        },
    },
    VerbalRootTag.__tablename__: {
        "meta": {},
        "data": {
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "explanation": "Explanation",
            "markers": "Markers",
            "syntactic_condition": "Syntactic Condition",
        },
    },
}

###############################################################################
