import pika
import traceback

from app import app
import pdb

class Publisher:
    def init(self, config):
        """
        Initializes configuration of publisher
        """
        self.config = config

    def publish(self, event):
        """
        Publishes messages to given queue
        """
        connection = None

        try:
            # Create channel and connection
            channel = self._create_channel()
            try:
                # Try to declare queue
                channel.queue_declare(queue='queue', durable=True)
            except:
                # recreate channel if queue exists.
                channel = self._create_channel()

            # Publish message to rabbitmq
            channel.basic_publish(exchange='', routing_key=self.config['routingKey'], body=event)
        except Exception as e:
            app.logger.warning('Error on message publish')
        finally:
            # If anything fails close connection
            if connection:
                connection.close()

    def _create_channel(self):
        """
        Creates connection with configured credentials and address.
        """
        credentials = pika.PlainCredentials(self.config['username'], self.config['password'])
        parameters = pika.ConnectionParameters(self.config['host'], self.config['port'], '/', credentials)
        connection = pika.BlockingConnection(parameters)

        return connection.channel()