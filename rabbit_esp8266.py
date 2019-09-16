"""
James Tregaskis
August 2019
client that parses and strips out mac addresses,
ignoring beacons; the data is
obtained from Sniffer on a connected esp8266 device
via USB (/dev/ttyUSB0 on pi)
The mac addreesses are sent via rabbitmq
v.2
Modified to send via direct (not fanout)
"""

import time
import pika
import serial
import sys
IP='10.10.10.9'

ser = serial.Serial('/dev/ttyUSB0', baudrate = 115200, timeout =1)
# this is a set to hold mac addresses picked up in this session
# I include my own mac address of my pc as I do not want it
# identified as a newly added mac address
# this is to announce newly spotted mac addresses
macSet = set()
# ignore appearance of my macbook, this is my machine's mac address
macSet.add('8c8590c317fa')

# set up rabbitmq
credentials = pika.PlainCredentials('bax', 's')
parameters = pika.ConnectionParameters('10.10.10.9',
								   5672,
								   '/',
								   credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='direct_logs3', exchange_type='direct')
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'


def konnect(theMessage):
    credentials = pika.PlainCredentials('bax', 's')
    parameters = pika.ConnectionParameters(IP,
                                        5672,
                                        '/',
                                        credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs3', exchange_type='direct')
    severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    channel.basic_publish(exchange='direct_logs3', routing_key=severity,body=str(theMessage))
    time.sleep(2)
    connection.close()

def broadcastMac(mac):
	print("newmac " + mac)
	konnect(mac)
	print("no. of mac addresses held: " +str(len(macSet)))


def collectDetails(mac):
	# this function will check if mac address is a new one
	# and if it is, send a rabbitmq message

	if mac not in macSet:
		macSet.add(mac)
		broadcastMac(mac)

while True:
	try:
		data = ser.readline().decode('ascii')
		print(data)
		# clean up and parse out the mac addresses
		if len(data) > 1:

			# formatted as follows:
			#DEVICE: 020fb5986c53 ==> [                              ??]  0400400e0100  11   0   0    -81
			#print("0         1         2         3         4        5          6         7         8         9")
			#print("012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901")
			#print (data)
			if int(data.find("DEVICE:")) !=-1 and int(data.find("DEVICE:")) !=0:

				foundAt = int(data.find("DEVICE:"))
				#print(foundAt)
				#print("the word DEVICE: found at " + str(foundAt))
				#print("mac " + data[foundAt+8:foundAt+20])
				collectDetails(data[foundAt+8:foundAt+20])
			if int(data.find("BEACON:")) !=-1 and int(data.find("BEACON:")) !=0:

				foundAt = int(data.find("BEACON:"))

				if str((foundAt)+8) != "<":
					#print("mac " + data[foundAt+61:foundAt+73])
					collectDetails(data[foundAt+61:foundAt+73])
				else:
					collectDetails(data[foundAt+8:foundAt+20])

			time.sleep(1)
	except UnicodeDecodeError:
		print("decode exception")
		pass
	except Exception as e:
		print(e)
		pass
