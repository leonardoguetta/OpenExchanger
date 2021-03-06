#!/usr/bin/env python
import wiringpi
import time

#Purpose: Test the Raspberry PI GPIO connectivity to the Pyramid Apex 5400 Bill Acceptor.
#PINOUT Configuration
#
#APEX              PI
#-----------------------------
#PIN 1 (PULSE)  --> Pin 18
#PIN 4 (Ground) --> Raspberry PI Ground (important to use the pi to standardize the ground)
#Pin 11 (12V)   --> DO NOT CONNECT TO PI (this should be connected to a 12v adapter)
#PIN 12 (Enable)--> DO NOT CONNECT TO PI (this should be tied to 12v Ground)
#
# APEX Configuration Sheet
# Pulse/Serial, 4 Pulses per dollar, Fast Pulse Speed, Lighted Bezel - Flashing, Currencies: 1, 5, 10, 20, 50, 100, Security Level: Low, Direction: All 4 ways
#
# A huge thank you to Mike Parks (https://helpouts.google.com/114808324731233563403/ls/b47f0efd3a3a4023) for his help getting this to work)
#
# Gregg Geil



#Constants
PIN = 18

#Setup Wiring PI Configuration
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(PIN, wiringpi.INPUT)

#Need to pull up to 3.3v since the Apex 5400 goes to 0 to mark a pulse
wiringpi.pullUpDnControl(PIN,wiringpi.PUD_UP)
pulses = 0
amount = 0
while 1:
 #1 will represent normal state, 0 will reprsent a pulse.
 if wiringpi.digitalRead(PIN) == 0:
  pulses = pulses + 1
  if pulses == 4:
	pulses = 0
	amount = amount + 1
  print 'Total Amount: ' + str(amount)
 time.sleep(.01)
