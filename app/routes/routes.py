import socket
import json
import asyncio

from collections import namedtuple

from app import app
from app.models.socket_model import SocketModel
from .socket_thread import SocketThread

# Set up Global Variables:
host = app.config['HOST']
port = int(app.config['PORT'])

async def parse_socket(host, port):
    """
    Connects to given port and listens for sockets.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gw_socket:
        gw_socket.bind((host, port))
        gw_socket.listen()
        app.logger.info('Listening to: %s:%s' % (str(host), str(port)))
        while True:
            gwConnection, gwAddress = gw_socket.accept()
            with gwConnection:
                app.logger.info('Received from:%s' % str(gwAddress))
                socket_thread = SocketThread(gwAddress, gwConnection)
                socket_thread.start()
                socket_thread.join()


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
    socket_tasks.cancel()
    app.logger.info('Closing Sockets. Bye')