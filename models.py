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


class SentenceTypeMeaningTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    description = Column(Text)


class SentenceTypeMeaningData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{SentenceTypeMeaningTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{SentenceTypeMeaningTag.__tablename__}_data'))
    tag = relationship(SentenceTypeMeaningTag.__qualname__, backref=backref('data'))


###############################################################################


class SentenceTypeStructureTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    description = Column(Text)


class SentenceTypeStructureData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{SentenceTypeStructureTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    markers = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{SentenceTypeStructureTag.__tablename__}_data'))
    tag = relationship(SentenceTypeStructureTag.__qualname__, backref=backref('data'))


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


class VerbalRootTypeTag(db.Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, index=True)
    tag = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    english_name = Column(String(255))
    description = Column(Text)


class VerbalRootTypeData(db.Model):
    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey(f'{VerbalRootTypeTag.__tablename__}.id'), nullable=False)
    language_id = Column(Integer, ForeignKey(f'{Language.__tablename__}.id'), nullable=False)
    example = Column(Text)
    iso_transliteration = Column(Text)
    sanskrit_translation = Column(Text)
    english_translation = Column(Text)
    explanation = Column(Text)
    markers = Column(Text)
    syntactic_clues = Column(Text)

    language = relationship(Language.__qualname__, backref=backref(f'{VerbalRootTypeTag.__tablename__}_data'))
    tag = relationship(VerbalRootTypeTag.__qualname__, backref=backref('data'))


###############################################################################


TAG_LIST = {
    SentenceTypeMeaningTag.__tablename__: ("अर्थानुसार-वाक्यप्रकार", "Sentence Type (Meaning)", SentenceTypeMeaningTag, SentenceTypeMeaningData),
    SentenceTypeStructureTag.__tablename__: ("रचनानुसार-वाक्यप्रकार", "Sentence Type (Structure)", SentenceTypeStructureTag, SentenceTypeStructureData),
    VoiceTag.__tablename__: ("क्रिया-वाच्य", "Voice", VoiceTag, VoiceData),
    PartsOfSpeechTag.__tablename__: ("शब्द-प्रकार", "Parts-of-Speech (POS)", PartsOfSpeechTag, PartsOfSpeechData),
    # "5": ("शब्द-रूप", "Morphology", None, None),
    VerbalTag.__tablename__: ("क्रियामूलक-कृद्", "Verbal", VerbalTag, VerbalData),
    TenseAspectMoodTag.__tablename__: ("क्रिया-कालादि", "Tense-Aspect-Mood (TAM)", TenseAspectMoodTag, TenseAspectMoodData),
    # "8": ("शब्द-समूह", "Group", None, None),
    DependencyTag.__tablename__: ("आश्रय", "Dependency", DependencyTag, DependencyData),
    VerbalRootTypeTag.__tablename__: ("धातुप्रकार", "Verbal Root Type", VerbalRootTypeTag, VerbalRootTypeData),
    # "11": ("कर्म-प्रधानता", "Ergativity", None, None)
}

TAG_SCHEMA = {
    SentenceTypeMeaningTag.__tablename__: {
        "meta": {},
        "data": {
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "markers": "Markers"
        },
    },
    SentenceTypeStructureTag.__tablename__: {
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
    VerbalRootTypeTag.__tablename__: {
        "meta": {},
        "data": {
            "example": "Example",
            "iso_transliteration": "ISO Transliteration",
            "sanskrit_translation": "Sanskrit Translation",
            "english_translation": "English Translation",
            "explanation": "Explanation",
            "markers": "Markers",
            "syntactic_clues": "Syntactic Clues",
        },
    },
}

###############################################################################
