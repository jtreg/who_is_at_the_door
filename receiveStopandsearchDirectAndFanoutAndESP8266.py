#!/usr/bin/env python
'''
Name: receiveStopandsearchDirectAndFanoutAndESP8266.py
James Tregaskis
Aug 2019
This is derived from code from tutorials as
https://www.rabbitmq.com/tutorials/tutorial-three-python.html
This will send machines across machines
Revised to use RabbitMQ
receiving stop and search data in direct mode
also
receiving twitter api data in fanout mode
also
receiving direct messages from esp8266

'''
import pika
import sys
import socket
hostname = socket.gethostname()
IP= '10.10.10.9'



credentials = pika.PlainCredentials('bax', 's')
parameters = pika.ConnectionParameters(IP,
                                   5672,
                                   '/',
                                   credentials)

# for the stop and search messages (via direct mode)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# for the twitter api messages
fanoutChannel = connection.channel()
fanoutChannel.exchange_declare(exchange='logs', exchange_type='fanout')
fanoutResult = fanoutChannel.queue_declare(queue='', exclusive=True)
fanoutQueue_name = fanoutResult.method.queue
fanoutChannel.queue_bind(exchange='logs', queue=queue_name)


#for the esp8266 messages
espchannel = connection.channel()
espresult = espchannel.queue_declare(queue='', exclusive=True)
espqueue_name = espresult.method.queue

severities =sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='direct_logs2',queue=queue_name,routing_key=severity)

for severity in severities:
    espchannel.queue_bind(exchange='direct_logs3',queue=espqueue_name,routing_key=severity)


print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    # skip first letter
    print(body.decode("utf-8"))
try:
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    fanoutChannel.basic_consume(
        queue=fanoutQueue_name, on_message_callback=callback, auto_ack=True)

    espchannel.basic_consume(
        queue=espqueue_name, on_message_callback=callback, auto_ack=True)


    channel.start_consuming()

    fanoutChannel.start_consuming()

    espchannel.start_consuming()

except:
	pass
