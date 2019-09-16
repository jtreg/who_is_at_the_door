#!/usr/bin/ python3
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import logging
'''
# James Tregaskis
# james@tregaskis.org
# March 1st 2019
----------------
 This takes value from GPIO pin 22 on the Raspberry Pi
 if pi 22 pressed shows one video
 upon release, it shows another video
 Rather than use mplayer, OMXPlayer uses the Raspberry
 Pi's GPU and runs better than mplayer.
 OmxPlayer is controlled by a wrapper, the code for the wrapper
 is provided by Will Price on Github. This wrapper
 sends messages from python via dbus to
 omxplayer which uses the GPU
 providing a nice stable responsive video
 The same basic code was used in the installation to run
 two different pairs of videos.
--------------------
'''
# create and configure logging module
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "willprice.log", level = logging.ERROR, format = LOG_FORMAT, filemode = 'w')

# this is called the root logger
logger = logging.getLogger()
logger.info("the first message as info")

import RPi.GPIO as GPIO    # Import RPi Library
# setup
GPIO.setmode(GPIO.BCM)   # Specify We Want to reference Physical pins
button1=22  # Descriptive Variable for pin 12
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP) # Set button1 as input and Activate pull up resistor



VIDEO_1_PATH = Path("Videos/ExDragonflyEyes.mp4")
VIDEO_2_PATH = Path("Videos/beach1.mp4")
player_log = logging.getLogger("Player 1")

'''
Alternate files used
ChannelsVIDEO_1_PATH = Path("Videos/ussrtestcard.mp4")
#VIDEO_2_PATH = Path("Videos/tvtestcard.mp4")
VIDEO_3_PATH = Path("Videos/ddrclip.mp4")
'''


player = OMXPlayer(VIDEO_1_PATH,args=['--loop'],dbus_name='org.mpris.MediaPlayer2.omxplayer1')
player.playEvent += lambda _: player_log.info("Play")
player.pauseEvent += lambda _: player_log.info("Pause")
player.stopEvent += lambda _: player_log.info("Stop")
player2 = OMXPlayer(VIDEO_2_PATH,args=['--loop'],dbus_name='org.mpris.MediaPlayer2.omxplayer2')

#logger.debug("-----------------------------------b-----------------")
player2.playEvent += lambda _: player_log.info("Play")
player2.pauseEvent += lambda _: player_log.info("Pause")
player2.stopEvent += lambda _: player_log.info("Stop")

# it takes about this long for omxplayer to warm up and start
# displaying a picture on a rpi3
player.hide_video()
sleep(2.5)
try:
	while True:
		if GPIO.input(button1)==0:
			#logger.debug("button 1 == 1")
			player.hide_video()
			player2.show_video()


		else:
			player2.hide_video()
			player.show_video()

except:
	logger.error
	player.quit()
	player2.quit()
	raise
else:
	player.quit()
	player2.quit()
	raise
finally:
	logger.info("finished")
	GPIO.cleanup()
