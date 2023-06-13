#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity
import models


class Place(BaseModel, Base):
    """ A place to stay 
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
    """

__tablename__ = 'places'
city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
name = Column(String(128), nullable=False)
description = Column(String(1024))
number_rooms = Column(Integer, default=0)
number_bathrooms = Column(Integer, default=0)
max_guest = Column(Integer, default=0)
price_by_night = Column(Integer, default=0)
latitude = Column(Float)
longitude = Column(Float)
reviews = relationship("Review", backref="place", cascade="delete")
amenities = relationship("Amenity", secondary="place_amenity",
                            viewonly=False)
amenity_ids = []
