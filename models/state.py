#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
import models
import os
from dotenv import find_dotenv, load_dotenv


class State(BaseModel, Base):
    """State class"""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    env_path = find_dotenv()
    load_dotenv(env_path)
    storage_type = os.getenv("HBNB_TYPE_STORAGE")
    storages = storage_type.split(",")
    for storage in storages:
        if storage == "db":
            cities = relationship("City", backref="state", cascade="all, delete")
        elif storage == "FileStorage":

            @property
            def cities(self):
                """Getter for cities"""
                cities = []
                for city in models.storage.all("City").values():
                    if city.state_id == self.id:
                        cities.append(city)
                return cities
