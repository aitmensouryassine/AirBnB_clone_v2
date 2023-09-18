#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """Represents the city class
    Class Attribute:
        __tablename__: the mapping table
        name: sqlalchemy String Column : the city name
        state_id: sqlalchemy String Column : the state identifier (FK)
    """
    __tablename__ = 'cities'

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
