#!/usr/bin/env python

#
# Example using Dynamic Payloads
# 
#  This is an example of how to use payloads of a varying (dynamic) size.
# 

from __future__ import print_function
import time
from RF24 import *
import RPi.GPIO as GPIO

irq_gpio_pin = None

radio = RF24(22, 0);

            
###PARSE COMMANDS###
	
def getOutput():
    output = getCommand(str(input('put command\n')))
    value = str(input('put value\n'))
    
    return output+'='+value
                    
def getCommand(x):
    switch = {
        '0' : "M",
        '1' : "U",
        '2' : "D",
        '3' : "L",
        '4' : "R"
        }
    return switch.get(x, 'N')


pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]
min_payload_size = 4
max_payload_size = 32
inp_role = 'none'
millis = lambda: int(round(time.time() * 1000))

radio.begin()
radio.enableDynamicPayloads()
radio.setRetries(5,15)
radio.printDetails()

print(' ************ Role Setup *********** ')


print('Role: Ping Out, starting transmission')
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1,pipes[1])

# forever loop
while 1:
# The payload will always be the same, what will change is how much of it we send.

	# First, stop listening so we can talk.
	radio.stopListening()

	send_payload = getOutput()
	
	radio.write(send_payload)

	# Now, continue listening
	radio.startListening()

	# Wait here until we get a response, or timeout
	started_waiting_at = millis()
	timeout = False
	while (not radio.available()) and (not timeout):
		if (millis() - started_waiting_at) > 500:
			timeout = True

	# Describe the results
	if timeout:
		print('failed, response timed out.')
	else:
		# Grab the response, compare, and send to debugging spew
		length = radio.getDynamicPayloadSize()
		receive_payload = radio.read(length)

		# Spew it
		print('got response size={} value="{}"'.format(length, receive_payload.decode('utf-8')))

	# Update size for next time.
	time.sleep(0.1)        



