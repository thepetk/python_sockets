import socket
import json
import asyncio
import pdb
from collections import namedtuple

from app import app
from .publisher import Publisher
from app.models.socket_model import SocketModel
from .routes_utils import create_session

# Set up Global Variables:
host = app.config['HOST']
port = int(app.config['PORT'])

# Create your publisher connection configuration
publisher_conf_dict = {
    'username': str(app.config['RMQ_USERNAME']),
    'password': str(app.config['RMQ_PASSWORD']),
    'host': str(app.config['RMQ_HOST']),
    'port': str(app.config['RMQ_PORT']),
    'routingKey':str(app.config['RMQ_QUEUE'])
}

publisher = Publisher()
publisher.init(publisher_conf_dict)

async def parse_socket(host, port):
    """
    Connects to given port and listens for sockets.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gw_socket:
        gw_socket.bind((host, port))
        gw_socket.listen()
        app.logger.info('Listening to: %s:%s' % (str(host), str(port)))
        while True:
            conn, addr = gw_socket.accept()
            with conn:
                app.logger.info('Received from:%s' % str(addr))
                data = conn.recv(2048)
                if not data:
                    break
                response= b'1'
                conn.sendall(response)
                conn.close()
                await service_connection(data)

async def service_connection(recv_data):
    '''
    Gets data from socket and stores it to DB. On fallback it saves event to RabbitMQ.
    '''
    if recv_data:
        # Decode data of received socket and convert it to namedtuple
        decoded_data = recv_data.decode('utf-8')
        decoded_event = json.loads(decoded_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        # Create new event on database
        new_socket = SocketModel(user_id = decoded_event.user_id,
                                address = decoded_event.address,
                                port = decoded_event.port)        
        try:
            db_session = create_session()
            db_session.merge(new_socket)
            db_session.commit()
            db_session.close()
            app.logger.info('Socket data Pushed Successfully')
        except Exception as e:
            publisher.publish(decoded_data)
            app.logger.info('Socket data Published to RabbitMQ')
    else:
        # Empty socket case.
        app.logger.warning('Socket empty. Connection closed')

# Create asyncio loop to await for incoming sockets
try:
    socket_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(socket_loop)
except RuntimeError as e:
    app.logger.warning(str(e))

socket_tasks = asyncio.gather(
    parse_socket(host, port)
)
try:
    socket_loop.run_forever()
except KeyboardInterrupt:
    app.logger.info('Canceling Tasks..')
    socket_loop.cancel()
    app.logger.info('Closing Sockets. Bye')