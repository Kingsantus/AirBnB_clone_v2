#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models import storage

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
                      )

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    user = relationship('User')
    city = relationship('City')

    if storage_type == 'db':
        reviews = relationship('Review', cascade='all, delete-orphan', backref='place')
        amenities = relationship('Amenity', secondary=place_amenity, viewonly=False, back_populates='place')


    else:
        @property
        def reviews(self):
            """ Getter attribute for reviews """
            all_reviews = models.storage.all(Review)
            place_reviews = [review for review in all_reviews.values() if review.place_id == self.id]
            return place_reviews

                @property
        def amenities(self):
            """ Getter attribute for amenities """
            all_amenities = storage.all(Amenity)
            place_amenities = [amenity for amenity in all_amenities.values() if amenity.id in self.amenity_ids]
            return place_amenities

        @amenities.setter
        def amenities(self, obj):
            """ Setter attribute for amenities """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
                storage.save()
