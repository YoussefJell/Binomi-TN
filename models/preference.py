#!/usr/bin/python
""" holds class Preference"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

if models.storage_t == 'db':
    user_preference = Table('user_preference', Base.metadata,
                            Column('preference_id', String(60),
                                   ForeignKey('preferences.id', onupdate='CASCADE',
                                              ondelete='CASCADE'),
                                   primary_key=True),
                            Column('user_id', String(60),
                                   ForeignKey('users.id', onupdate='CASCADE',
                                              ondelete='CASCADE'),
                                   primary_key=True))


class Preference(BaseModel, Base):
    """Representation of Preference """
    if models.storage_t == 'db':
        __tablename__ = 'preferences'
        name = Column(String(128), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False) 
        users = relationship("User",
                             secondary=user_preference,
                             viewonly=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        name = ""
        user_ids = []

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    if models.storage_t != 'db':
        @property
        def users(self):
            """getter attribute returns the list of User instances"""
            from models.user import User
            user_list = []
            all_users = models.storage.all(User)
            for user in all_users.values():
                if user.preference_id == self.id:
                    user_list.append(user)
            return user_list
