from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class ReturnCar(Base):
    __tablename__ = 'returned_car'

    id = Column(Integer, primary_key = True )
    trace_id = Column(String(250), nullable=False)
    car_id = Column(Integer, nullable=False )
    kilometers = Column(Integer, nullable=False)
    gas_used = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    rent_duration = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, car_id, kilometers, gas_used, cost, rent_duration, trace_id):
        """ Initializes a car return """
        self.car_id = car_id
        self.trace_id = trace_id
        self.kilometers = kilometers
        self.gas_used = gas_used
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.cost = cost
        self.rent_duration = rent_duration

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['car_id'] = self.car_id
        dict['trace_id'] = self.trace_id
        dict['kilometers'] = self.kilometers
        dict['gas_used'] = self.gas_used
        dict['cost'] = self.cost
        dict['rent_duration'] = self.rent_duration
        dict['date_created'] = self.date_created

        return dict