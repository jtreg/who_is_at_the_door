#!/usr/bin/env python
'''
Name receive_hcsro4.py
James Tregaskis
Aug 2019
This is derived from code from tutorials as
https://www.rabbitmq.com/tutorials/tutorial-three-python.html
This will send tweets across machines sent as a fanout
The hc-sr04 proximity detector will activate upon readings sensed
and the resultant events sent as rabbitmq messages.
'''
import pika
import RPi.GPIO as GPIO
import time
import pygame
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO mappings
TRIG = 18
ECHO = 23
RED = 4
YELLOW = 17
GREEN = 27
CRADLE = 22
MP3_1 = 24
MP3_2 = 25
MP3_3 = 12
MP3_4 = 16
MP3_5 = 26

NEAR=30
FAR=40
FURTHEST=50

start=0
end=0
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(YELLOW,GPIO.OUT)
GPIO.setup(MP3_1,GPIO.OUT)
GPIO.setup(MP3_2,GPIO.OUT)
GPIO.setup(MP3_3,GPIO.OUT)
GPIO.setup(MP3_4,GPIO.OUT)
GPIO.setup(MP3_5,GPIO.OUT)
GPIO.setup(RED,GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CRADLE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# this is connection setup for rabbitmq messages
credentials = pika.PlainCredentials('bax', 's')
parameters = pika.ConnectionParameters('10.10.10.9',
										5672,
										'/',
										credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)


def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    sig_time = end-start

    #CMS:
    distance = sig_time / 0.000058
    distance = sig_time / 0.000058
    #inches:
    #distance = sig_time / 0.000148
    #print('Distance: {} centimeters'.format(distance))
    return distance

#print(' [*] Waiting for logs. To exit press CTRL+C')

while True:
    distance=0
    distance = get_distance()
    time.sleep(0.05)
    # print(distance)

    if distance >= FURTHEST:
        green_light()
        print(body)
        # mp3_3()
    elif FURTHEST > distance > NEAR:
        yellow_light()
        print("message 3")
        # mp3_1()
    elif distance <= NEAR:
        print("message 2")
        # mp3_2()
        red_light()


def callback(ch, method, properties, body):
    distance=0
    distance = get_distance()
    time.sleep(0.05)
    if distance >= FURTHEST:
        green_light()
        print(body)
        # mp3_3()
    elif FURTHEST > distance > NEAR:
        yellow_light()
        print("message 3")
        # mp3_1()
    elif distance <= NEAR:
        print("message 2")
        # mp3_2()
        red_light()


channel.basic_consume(
	queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
