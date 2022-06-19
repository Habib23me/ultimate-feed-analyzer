import pika, sys, os
import ssl
import sys
from data_model.activity import *
from services.analyzer import *


def init():
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    credentials = pika.PlainCredentials(os.environ['BROKER_USERNAME'], os.environ['BROKER_PASSWORD'])
    params=pika.ConnectionParameters(
        host=os.environ['BROKER_HOST'],
        port=os.environ['BROKER_PORT'],
                                       virtual_host='/',
                                       credentials=credentials,
                                       ssl_options=pika.SSLOptions(context)
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()



    channel.queue_declare(queue='activity',durable=True)

    def callback(ch, method, properties, body):
        print(type(body.decode()))
        print(" [x] Received %r" % body.decode())
        activity:Activity = activity_from_str(body.decode());
        analyseActivity(activity)

    channel.basic_consume(queue='activity', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()