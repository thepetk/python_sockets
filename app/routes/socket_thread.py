import socket
import threading
import json

from time import sleep
from collections import namedtuple

from app import app, logger, db
from app.models.socket_model import SocketModel
from .routes_utils import create_session
from .publisher import Publisher

publisher_conf_dict = {
    'username': str(app.config['RMQ_USERNAME']),
    'password': str(app.config['RMQ_PASSWORD']),
    'host': str(app.config['RMQ_HOST']),
    'port': str(app.config['RMQ_PORT']),
    'routingKey':str(app.config['RMQ_QUEUE'])
}

class SocketThread(threading.Thread):
    """
    Instance of socket thread.
    """

    def __init__(self, gwAddress, gwConnection):
        threading.Thread.__init__(self)
        self.gwConnection = gwConnection
        app.logger.info("Received from: %s" % str(gwAddress))

    def run(self):
        data = self.gwConnection.recv(2048)
        response= b'1'
        self.gwConnection.send(response)  # Should be ready to write
        self.gwConnection.close()
        self.service_connection(data)

    def service_connection(self, recv_data):
        '''
        Gets data from socket and stores it to DB. On fallback it saves event to Kafka.
        '''
        if recv_data:
            # Fix keys of json and parse received data as namedtuple
            decoded_data = recv_data.decode('utf-8')
            decoded_event = json.loads(decoded_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            # Create new event on database
            new_socket = SocketModel( user_id = decoded_event.user_id,
                                    address = decoded_event.address,
                                    port = decoded_event.port)
            try:
                thread_session = create_session()
                thread_session.merge(new_socket)
                thread_session.commit()
                thread_session.close()
                app.logger.info('Socket data Pushed Successfully')
            except Exception as e:
                publisher = Publisher()
                publisher.init(publisher_conf_dict)
                publisher.publish(decoded_data)
                app.logger.info('Event Published to RabbitMQ')
        else:
            # Empty socket case.
            app.logger.warning('Socket empty. Connection closed')
