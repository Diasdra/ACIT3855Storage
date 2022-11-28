from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class RentCar(Base):
    __tablename__ = 'rented_car'

    id = Column(Integer, primary_key = True )
    trace_id = Column(String(250), nullable=False)
    car_id = Column(Integer, nullable=False)
    car_type = Column(String(250), nullable=False)
    location = Column(String(250), nullable=False)
    mileage = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    passenger_limit = Column(Integer, nullable=False)

    def __init__(self, car_id, car_type, location, mileage, passenger_limit, trace_id):
        """ Initializes a rented car """
        self.car_id = car_id
        self.car_type = car_type
        self.trace_id = trace_id
        self.location = location
        self.mileage = mileage
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.passenger_limit = passenger_limit

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['car_id'] = self.car_id
        dict['car_type'] = self.car_type
        dict['trace_id'] = self.trace_id
        dict['location'] = self.location
        dict['mileage'] = self.mileage
        dict['passenger_limit'] = self.passenger_limit
        dict['date_created'] = self.date_created

        return dict
