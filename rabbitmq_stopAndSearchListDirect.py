'''
Name: rabbitmq_stopAndSearchListDirect.py
James Tregaskis
Aug 2019
This collects data from HM Government website for stop and search data.
The data can be retrieved up to 3 months ago and will include details of where
the event ocurred, description of suspect's racial profile
and the outcome.
The data is sent on via rabbitmq to the listening program;
receiveStopandsearchDirectAndFanoutAndESP8266.py


# The data is derived from the metropolitan police api
https://police-api-client-python.readthedocs.io/en/develop/reference/stop_and_search.html
revised to use RabbitMQ
# in Direct mode (not fanout)
'''
from urllib import request, parse
import json
from pprint import pprint
import sys,time,random
import tkinter as tk
import pika
import socket
import time


IP='10.10.10.9'

credentials = pika.PlainCredentials('bax', 's')
parameters = pika.ConnectionParameters(IP,
                                   5672,
                                   '/',
                                   credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

# to slow down the display of the messages to help
# viewer read them more easily
def sprint(str):
   for c in str + '\n':
     sys.stdout.write(c)
     sys.stdout.flush()
     time.sleep(1./90)

while True:
    # note the data is available older than 3 months ago (yyyy-mm)
    url = "https://data.police.uk/api/stops-" + "street?lat=51.5319&lng=0.0037&date="
    url = url.strip("\n")
    url = url + "2019-03"

    u = request.urlopen(url)
    resp = json.loads(u.read().decode('utf-8'))

    # to display slowly (currently commented out)
    # sprint(str(resp))

    for message in str(resp).split(","):
        print(message)
        channel.basic_publish(exchange='direct_logs2', routing_key=severity,body=message)

        time.sleep(4)
connection.close()
