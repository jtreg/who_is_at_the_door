'''
___________
James Tregaskis
james@tregaskis.org
August 2019
___________
Purpose:
___________
this is to send messages for the standardised
wired connections to the intercom switches:
1. the cradle switches
2. Buttons 1-3
(to all receiving rabbitmq servers)
when the state of the button changes the message is sent
This will run on all 6 intercoms
and send back out to all the other intercoms.
'''
import RPi.GPIO as GPIO
import time
import pika
import sys
import socket
#hostname = socket.gethostname()
IP='10.10.10.9' #socket.gethostbyname(hostname)''

GPIO.setmode(GPIO.BCM)
# gpio pins (same on all intercoms)
cradle=22
button1=5
button2=6
button3=13
lastmessageWas=''
cradleState =False
GPIO.setup(cradle, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def konnect(theMessage):
    '''
    this routine takes care of the connection to rabbitmq.
    we assume that the ip address running the rabbitmq server is
    already running on 10.10.10.9
    which is via a private router independent of the college WiFi
    all the connections to rabbitmq use the same WiFi connection
    (in my case it is ssid = jamesieTrip)
    '''
    credentials = pika.PlainCredentials('bax', 's')
    parameters = pika.ConnectionParameters('10.10.10.9',
                                        5672,
                                        '/',
                                        credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    channel.basic_publish(exchange='logs', routing_key='', body=str(theMessage))
    print("sendin message " + theMessage)
    connection.close()
try:
    while True:
        # if the handset is lifted...
        # make sure we dont send the message more than once if it was the same thing
        if GPIO.input(cradle) == 0 and (GPIO.input(button1) == 1 and GPIO.input(button2) == 1 and GPIO.input(button3) == 1):
            if lastmessageWas != 'cradle_up' and cradleState == True:
                konnect('cradle_up')
                lastmessageWas = 'cradle_up'
                cradleState = False
        elif GPIO.input(cradle) == 0 and (GPIO.input(button1) == 0 and GPIO.input(button2) == 1 and GPIO.input(button3) == 1):
            if 'button1' != lastmessageWas:
                #print('button1 pressed')
                konnect('button1')
                lastmessageWas = 'button1'
        elif  GPIO.input(cradle) == 0 and GPIO.input(button1) == 1 and GPIO.input(button2) == 0 and GPIO.input(button3) == 1:
            if 'button2' != lastmessageWas:
                #print('button2 pressed')
                konnect('button2')
                lastmessageWas = 'button2'
        elif  GPIO.input(cradle) == 0 and GPIO.input(button1) == 1 and GPIO.input(button2) == 1 and GPIO.input(button3) == 0:
            if 'button3' != lastmessageWas:
                #print('button3 pressed')
                konnect('button3')
                lastmessageWas = 'button3'
        # if handset is down logic...
        elif GPIO.input(cradle) == 1 and (GPIO.input(button1) == 1 and GPIO.input(button2) == 1 and GPIO.input(button3) == 1):
            if lastmessageWas != 'cradle_down' and cradleState == False:
                #print('cradle_down')
                konnect('cradle_down')
                lastmessageWas = 'cradle_down'
                cradleState = True

        elif GPIO.input(cradle) == 1 and (GPIO.input(button1) == 0 and GPIO.input(button2) == 1 and GPIO.input(button3) == 1):
            if (lastmessageWas != 'button1'):
                #print('button1 pressed')
                konnect('button1')
                lastmessageWas = 'button1'

        elif  GPIO.input(cradle) == 1 and GPIO.input(button1) == 1 and GPIO.input(button2) == 0 and GPIO.input(button3) == 1:
            if 'button2' != lastmessageWas:
                #print('button2 pressed')
                konnect('button2')
                lastmessageWas = 'button2'

        elif  GPIO.input(cradle) == 1 and GPIO.input(button1) == 1 and GPIO.input(button2) == 1 and GPIO.input(button3) == 0:
            if 'button3' != lastmessageWas:
                #print('button3 pressed')
                konnect('button3')
                lastmessageWas = 'button3'


except Exception as e:
    print(e)
    pass
    GPIO.cleanup()
