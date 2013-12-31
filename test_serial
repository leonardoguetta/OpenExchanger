#!/usr/bin/env python
import wiringpi
import time

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
