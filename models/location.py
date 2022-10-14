#!/usr/bin/python
""" holds class Location"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


class Location(BaseModel, Base):
    """Representation of Location """
    if models.storage_t == 'db':
        __tablename__ = 'locations'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Location"""
        super().__init__(*args, **kwargs)
