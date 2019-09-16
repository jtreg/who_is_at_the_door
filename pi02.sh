#!/bin/bash
# Name: pi02 
# this is startup script on machine
# called by /etc/rc.local
xterm  -fa 'Monospace' -fs 14  -e "python3 emit_twitter.py"  &
xterm   -e "python3 rabbit_esp8266.py"  &
xterm   -e "python3 rabbitmq_stopAndSearchListDirect.py"  &
python3 receive_gpio_fanout.py &
python3 send_gpio_presses.py &
xterm  -fa 'Monospace' -fs 20 -maximized  -e "python3 receiveStopandsearchDirectAndFanoutAndESP8266.py info"
