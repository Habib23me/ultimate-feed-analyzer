from util import Singleton
import pika
import sys
import os
import ssl
from dotenv import load_dotenv
# from Environment import EpsilonGreedyEnvironment
import json

load_dotenv()


class RabbitMQService(metaclass=Singleton):

    def init(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.credentials = pika.PlainCredentials(
            os.environ['BROKER_USERNAME'], os.environ['BROKER_PASSWORD'])
        params = pika.ConnectionParameters(
            host=os.environ['BROKER_HOST'],
            port=os.environ['BROKER_PORT'],
            virtual_host='/',
            credentials=self.credentials,
            ssl_options=pika.SSLOptions(self.context)
        )
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        print("Connected to RabbitMQ Service")

    def subscribe(self, queue, callback):
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_consume(
            queue=queue, auto_ack=True, on_message_callback=callback)
        print("Subscribed to Queue: ", queue)
        return {}

    def send(self, queue, message):
        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue,
                                   body=message)
        print("Sent message to queue: ", queue)
        print("Message: ", message)

    def close_connection(self):
        self.connection.close()
        print("Closed RabbitMQ Service")

    def start_consuming(self):
        self.channel.start_consuming()
