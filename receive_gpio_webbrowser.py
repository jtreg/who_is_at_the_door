"""
Name: receive_gpio_webbroswer.py
Author: James Tregaskis
Date: Aug 2019

This program receives messages sent via rabbitmq_stopAndSearchListDirect
based on proximal hc-sro4 messages, button presses and phone cradle release and closure
The resultant messages initiate virtual key presses to a browser to change the
tab comprising the streamed camera content from installed web cameras
"""

import pyautogui
import webbrowser
import os
from time import sleep
import pika

IP= '10.10.10.9'
'''
These IP addresses are hard coded as they relate to the
static IP addresses of installed web cameras
'''
webbrowser.open("http://10.10.10.7:8081",new=1)
webbrowser.open("http://10.10.10.98:8081",new=2)
webbrowser.open("http://10.10.10.99:8081",new=2)
#webbrowser.open("http://10.10.10.100:8081",new=2)
lastmessage =''
sleep(20)

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

print(' [*] Waiting for logs. To exit press CTRL+C')

def shiftTab(n):
	for x in range (0, n):
		pyautogui.hotkey('CTRL','shift', 'tab')

def callback(ch, method, properties, body):
	body = body.decode("utf-8")
	#print(body)
	if body != lastmessage:
		if body == 'cradle_up':
			shiftTab(1)
			sleep(2)
			print("cradle up received")
		elif (body == 'button1' or body == 'button2' or body == 'button3'):
			shiftTab(2)
			sleep(2)
			print("button received")

		elif (body == 'nearest' or body == 'middledistance'):
			shiftTab(1)
			sleep(2)
			print("else received")

		#print(body)



channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
