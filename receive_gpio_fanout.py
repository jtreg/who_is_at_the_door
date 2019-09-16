#!/usr/bin/env python
'''
Name: receive_gpio_fanout.py
James Tregaskis
Aug 2019
This is derived from code from rabbitmq.com tutorials as
https://www.rabbitmq.com/tutorials/tutorial-three-python.html
This will listen for messages machines and play a randomised
audio file relating to the theme of surveillance in this particuar
installation. The cradle_up message is ignored as this would be sent
too often, instigated by gallery visitors.
'''
import pika
import socket
import playRandomMessage


IP= '10.10.10.9'

credentials = pika.PlainCredentials('bax', 's')
parameters = pika.ConnectionParameters(IP,
                                   5672,
                                   '/',
                                   credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

# print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(body.decode("utf-8"))
    if body != 'cradle_up':
        playRandomMessage.playMp3()

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
