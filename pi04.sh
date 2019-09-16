#!/bin/bash
# Name: pi04
# this is startup script on machine
# called by /etc/rc.local
python3 send_hcsro4_messages.py &
python3  receive_gpio_fanout.py  &
python3  send_gpio_presses.py  &
