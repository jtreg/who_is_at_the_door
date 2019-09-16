#!/usr/bin/python
'''
Name: emit_twitter.py
James Tregaskis
Aug 2019
The rabbitmq code portion here is derived from code from tutorials as
https://www.rabbitmq.com/tutorials/tutorial-three-python.html
This will initiate a Twitter API search, based on a number of surveillance-related
search terms. The resultant tweets are sent as messages in a 'fanout' mode to all
listening machines
'''
import pika
import sys
import tweepy
import time
import re
#import pyttsx3
#import engineio
import os
import string
import socket
import random
randWord = ["surveillance", "dystopian", "privacy", "neoliberalism", "osint", "hackers", "panoptic", "NSA", "GCHQ", "dragonfly","pwned", "sousurveillance", "panspectric"]
random.choice(randWord)

IP= '10.10.10.9'

#engineio = pyttsx3.init()
previousSaid =""
saidThis=""
key ="tXEGOPLlEgZ1kA67RBjsMEhj2"
secret = "3YgPr96luvQtZZYXsLZTFUJLgRBCpEdzrkqdwlQjZgFYc2CxWt"
AccessToken = "988405340785037312-nDszdJ9IumznsUdhN828OjmVByKG0I2"
AccessTokenSecret="jtvXxs5DKlBNnCa2Sy2ko0KOLSViqxjzM5dSREDx6uycz"

auth = tweepy.OAuthHandler(key,secret)
auth.set_access_token(AccessToken, AccessTokenSecret)

api = tweepy.API(auth)

#pika setup
credentials = pika.PlainCredentials('bax', 's')
parameters = pika.ConnectionParameters(IP,
									5672,
									'/',
									credentials)
connection = pika.BlockingConnection(parameters)
#connection = pika.BlockingConnection(
#    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

try:

	searchword = random.choice(randWord)
	for tweet in tweepy.Cursor(api.search,
								q=searchword,
								count= 20,
								#result_type="recent",
								include_entities=False,
								lang="en").items():

		#print ("----------------- " + searchword + " --------------------")
		random.choice(randWord)
		searchword = random.choice(randWord)
		saidThis = tweet.text
		#out = saidThis.translate(string.maketrans("",""),string.punctuation)

		#regax filter to clean out any urls (I don't want them displayed!)
		saidThis = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', saidThis)
		# this is where tweet is sent as a message

		saidThis = saidThis.replace(" " , "_")
		if previousSaid != saidThis:
			print(saidThis)
			os.system("espeak -v en-sc+f1 -k20 -p90 -l -s80 " + saidThis )
			channel.exchange_declare(exchange='logs', exchange_type='fanout')
			channel.basic_publish(exchange='logs', routing_key='', body=str(saidThis))
			previousSaid = saidThis
			time.sleep(1)
except KeyboardInterrupt:
		print("closing...")

		connection.close()
except Exception as e:
		print(e)
		connection.close()
finally:
	connection.close()
