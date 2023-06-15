#!/usr/bin/python3
"""This module defines the User class"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes:
    email = ''
    password = ''
    first_name = ''
    last_name = ''
    """

    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    places = relationship("Place", backref="user", cascade="all, delete-orphan")
    reviews = relationship("Review", backref="user", cascade="all, delete-orphan")
