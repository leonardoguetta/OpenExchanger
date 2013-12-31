#!/usr/bin/env python
import wiringpi
import time

#Purpose: Test the Raspberry PI GPIO connectivity to the Pyramid Apex 5400 Bill Acceptor.
#PINOUT Configuration
#
#APEX              PI
#-----------------------------
#PIN 1 (PULSE)  --> Pin 18
#PIN 4 (Ground) --> Raspberry PI Ground (important tu use the pi to standardize the ground)
#Pin 11 (12V)   --> DO NOT CONNECT TO PI (this should be connected to a 12v adapter)
#PIN 12 (Enable)--> DO NOT CONNECT TO PI (this should be tied to 12v Ground)
#
# APEX Configuration Sheet
# Pulse/Serial, 4 Pulses per dollar, Fast Pulse Speed, Lighted Bezel - Flashing, Currencies: 1, 5, 10, 20, 50, 100, Security Level: Low, Direction: All 4 ways

#Constants
PIN = 18

#Setup Wiring PI Configuration
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(PIN, wiringpi.INPUT)

#Need to pull up to 3.3v since the Apex 5400 goes to 0 to mark a pulse
wiringpi.pullUpDnControl(PIN,wiringpi.PUD_UP)

while 1:
 print wiringpi.digitalRead(PIN)
 time.sleep(.1)
