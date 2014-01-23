#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

def main():

    # tell the GPIO module that we want to use the 
    # chip's pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # setup pin 25 as an output
    GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(24,GPIO.OUT)
    #GPIO.setup(25,GPIO.OUT)


   # GPIO.output(25,True)

    while True:
        if GPIO.input(23):
             # the button is being pressed, so turn on the green LED
             # and turn off the red LED
            # GPIO.output(24,True)
            # GPIO.output(25,False)
             print "button true"
        else:
             # the button isn't being pressed, so turn off the green LED
             # and turn on the red LED
            # GPIO.output(24,False)
            # GPIO.output(25,True)
             print "button false"

        time.sleep(0.1)

    print "button pushed"

    GPIO.cleanup()



if __name__=="__main__":
    main()

