import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from rent_car import RentCar
from return_car import ReturnCar
import datetime
import logging
import uuid
from logging import config
import requests
import yaml
import json

from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread


with open('app_conf.yml', 'r') as f:
  app_config = yaml.safe_load(f.read())
  db_config = app_config['datastore']

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)


DB_ENGINE = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['hostname']}:{db_config['port']}/{db_config['db']}")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def rent_car(body):
    """ Receives a car rental application """

    session = DB_SESSION()

    car_rent = RentCar(body['car_id'],
                       body['car_type'],
                       body['location'],
                       body['mileage'],
                       body['passenger_limit'],
                       body['trace_id'])

    session.add(car_rent)
    session.commit()
    session.close()

    logger.debug(f'Stored event "rent car" request with a trace id of {body["trace_id"]}')

    return NoContent, 201


def return_car(body):
    """ Receives a car return form """

    session = DB_SESSION()

    carReturn = ReturnCar(body['car_id'],
                   body['kilometers'],
                   body['gas_used'],
                   body['cost'],
                   body['rent_duration'],
                   body['trace_id'])

    session.add(carReturn)

    session.commit()
    session.close()

    logger.debug(f'Stored event "return car" request with a trace id of {body["trace_id"]}')

    return NoContent, 201

def get_car_returns(timestamp):
    """ Gets new returns after the timestamp """
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    readings = session.query(ReturnCar).filter(ReturnCar.date_created >=timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for Car Returns readings after %s returns %d results" %(timestamp, len(results_list)))

    return results_list, 200

def get_car_rentals(timestamp):
    """ Gets new rentals after the timestamp """
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    readings = session.query(RentCar).filter(RentCar.date_created >=timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for Car Rentals readings after %s returns %d results" %(timestamp, len(results_list)))

    return results_list, 200

def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    
    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', reset_offset_on_start=False, auto_offset_reset=OffsetType.LATEST)
    
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "return_car": # Change this to your event type
            #logger.info(f'Recived payload of return car: {payload}')
            return_car(payload)
        elif msg["type"] == "rent_car": # Change this to your event type
            # Store the event2 (i.e., the payload) to the DB
            #logger.info(f'Recived payload of rent car: {payload}')
            rent_car(payload)
        # Commit the new message as being read
        consumer.commit_offsets()



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

logger = logging.getLogger('basicLogger')
logger.debug("debug message")
logger.info(f"Connecting to DB. Hostname: {db_config['hostname']}, Port: {db_config['port']}")

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
