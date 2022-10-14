#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=False)
        location_id = Column(String(60), ForeignKey(
            'locations.id'), nullable=False)
        budget = Column(Integer, nullable=False, default=0)
        preferences = relationship("Preference", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        description = ""
        location_id = ""
        sex = ""
        budget = 0

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        # if name == "password":
        # value =
        super().__setattr__(name, value)
