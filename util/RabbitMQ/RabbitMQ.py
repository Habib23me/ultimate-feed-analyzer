from util.Singleton import Singleton
import pika
import sys
import os
import ssl
from dotenv import load_dotenv
# from Environment import EpsilonGreedyEnvironment
import json
from data_model.activity import *
from services.analyzer import *

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
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(queue=queue,auto_ack=True,on_message_callback=callback)
        print("Subscribed to Queue: ", queue)
        return {}

    def send(self, queue, message):
        self.channel.queue_declare(queue=queue)
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

    def new_activity_callback(ch, method, properties, body):
        print(type(body.decode()))
        print(" [x] Received %r" % body.decode())
        activity:Activity = activity_from_str(body.decode());
        analyseActivity(activity)

    # {
    #   activity_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
    #   user_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
    #   score: 0.8,
    # }
    # {
    #   user_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
    # }
    def get_feed_callback(ch, method, properties, body):
        print(" [x] Received %r" % body)


    # {
    #   activity_id: 4e0fd601-4ecf-471a-ac90-e71db0e68593,
    #   user_id: 84c3e94e-ce0d-4721-8443-370b0325abd0,
    #   reward: 0.8,
    # }
    def record_result_callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        parsed_body = json.loads(body)

    # env = EpsilonGreedyEnvironment()
    # env.record_result(parsed_body['activity_id'], parsed_body['reward'])