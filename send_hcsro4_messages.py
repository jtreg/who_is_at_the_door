'''
___________
James Tregaskis
james@tregaskis.org
August 2019
___________
Purpose:
___________
This is to send rabbitmq messages to other machines
based on the proximity readings each machine's attached
HC-SR04 proximity detector
(sent to all receiving rabbitmq servers)
This will run on all 6 intercoms

'''
import RPi.GPIO as GPIO
import time
import pika
import sys
import os
IP='10.10.10.9'
machineName=str(os.uname().nodename)

GPIO.setmode(GPIO.BCM)
iveSaidItOnce=0
cradleLiftedAlready=0
TRIG = 18
ECHO = 23
'''
led lights for indication of how close
person is
'''
RED = 4
YELLOW = 17
GREEN = 27
cradle  = 22
MP3_1 = 24
MP3_2 = 25
MP3_3 = 12
MP3_4 = 16
MP3_5 = 26


lastmessageWas=''
cradleState =False
NEAR=50
FAR=80
FURTHEST=150

start=0
end=0
# GPIO pins setup
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
GPIO.setup(cradle, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(cradle, GPIO.RISING)

'''
this procedure manages the connection and message sending to
rabbitmq server (running on pi02; 10.10.10.9)
'''
def konnect(theMessage):
    credentials = pika.PlainCredentials('bax', 's')
    parameters = pika.ConnectionParameters(IP,
                                        5672,
                                        '/',
                                        credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    channel.basic_publish(exchange='logs', routing_key='', body=str(theMessage))
    connection.close()



def green_light():
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(RED, GPIO.LOW)

def yellow_light():
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.HIGH)
    GPIO.output(RED, GPIO.LOW)

def red_light():
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(RED, GPIO.HIGH)

'''
hc-sr04 calculate distance
'''
def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    sig_time = end-start

    #Centimetres                                                                                                                                                                                                                                                                                         :
    distance = sig_time / 0.000058

    return distance

try:
    while True:
        distance=0
        distance = get_distance()
        time.sleep(0.05)
        # print(distance)

        if distance >= FURTHEST:
            if 'furthest' != lastmessageWas:
                time.sleep(2)
                konnect('furthest')
                green_light()
                print("furthest " + machineName)
                lastmessageWas = 'furthest'
        elif distance < FURTHEST and distance >= NEAR:
            if 'middledistance' != lastmessageWas:
                time.sleep(2)
                konnect('middledistance')
                yellow_light()
                print("middledistance " + machineName)
                lastmessageWas = 'middledistance'
        elif distance < NEAR:
            if 'nearest' != lastmessageWas:
                time.sleep(2)
                konnect('nearest')
                red_light()
                print("nearest " + machineName)
                lastmessageWas = 'nearest'
except Exception as e:
    print(e)
    GPIO.cleanup()
finally:
    GPIO.cleanup()
