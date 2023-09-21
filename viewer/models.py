#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Models

@author: Hrishikesh Terdalkar
"""

###############################################################################

from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship, backref

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

###############################################################################
# Create database connection object

db = SQLAlchemy()

###############################################################################
# Database Models


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    hash = Column(String(255), nullable=False)


###############################################################################


class BaseMeta(db.Model):
    id = Column(Integer, primary_key=True)
    headword = Column(String(255), nullable=False, index=True)
    text = Column(String(255), nullable=False)


class BaseData(db.Model):
    id = Column(Integer, primary_key=True)
    short = Column(String(255), nullable=False)
    label = Column(String(255), nullable=False)


###############################################################################
