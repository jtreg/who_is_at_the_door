
#!/bin/bash
# Name: pi01
# this is startup script on machine
# called by /etc/rc.local
python3 ~/send_hcsro4_messages.py &
python3 ~/receive_ESP8266.py info &
python3  ~/receive_gpio_fanout.py &
python3  ~/send_gpio_presses.py  &
cd face
python  face_tracker_picam.py
