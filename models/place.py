#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy import ForeignKey
from models import storage_type


class Place(BaseModel, Base):
    """ A place to stay
    Class Attributes:
        __tablename__ : the mapping table
        city_id: String
        user_id: String
        name: String
        description: String
        number_rooms: Integer
        number_bathrooms : Integer
        max_guest: Integer
        price_by_night: Integer
        latitude: Float
        longitude: Float
    """
    __tablename__ = 'places'

    if storage_type != 'db':
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
    else:
        city_id = Column(String(60), ForeignKey('cities.id'),
                         nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'),
                         nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
