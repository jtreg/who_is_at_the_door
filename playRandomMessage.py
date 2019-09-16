'''
Name: playRandomMessage.py
James Tregaskis
August 2019
This file is imported by receive_gpio_fanout.py
to play a randomised audio file
'''

import time
import pygame
import random
# location of audio files on Pi
filePrefix='/home/pi/Music/'

def playMp3():
    filename=filePrefix + str(random.randint(1,31)) + '.mp3'
    print("playing " + filename)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    time.sleep(3.5)

try:

    playMp3()
except Exception as e:
    print(e)
