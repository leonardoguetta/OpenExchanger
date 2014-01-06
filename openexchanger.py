#!/usr/bin/python

# OpenExchanger v.01
# January 2, 2014
# Written by Gregg Geil
# BSD license, all text above must be included in any redistribution
#

#
# AdaFruit CharLCD Plate     - https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git
# AdaFruit Thermal Printer   - https://github.com/adafruit/Adafruit-Thermal-Printer-Library
# NewSoftSerial 			 - http://arduiniana.org/NewSoftSerial/NewSoftSerial10c.zip (Required for AdaFruit Thermal Printer)
#
# Influenced by Sheldon Hartling's Radio.PY
#
# Bill Acceptor Configuration / Tips
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






#dependancies
from Adafruit_I2C          import Adafruit_I2C
from Adafruit_MCP230xx     import Adafruit_MCP230XX
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from datetime              import datetime
from subprocess            import *
from time                  import sleep, strftime
from Queue                 import Queue
from threading             import Thread
from Adafruit_Thermal 	   import Adafruit_Thermal

import smbus
import simplejson
import requests
import wiringpi

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
LCD = Adafruit_CharLCDPlate()

# Define a queue to communicate with worker thread
LCD_QUEUE = Queue()

#Constants
VALIDATOR_PIN = 18 #For the Bill Acceptor Pulse Pin

#Setup Wiring PI Configuration
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(VALIDATOR_PIN, wiringpi.INPUT)
wiringpi.pullUpDnControl(VALIDATOR_PIN,wiringpi.PUD_UP)

# ----------------------------
# WORKER THREAD
# ----------------------------

# Define a function to run in the worker thread
def update_lcd(q):
   
   while True:
      msg = q.get()
      # if we're falling behind, skip some LCD updates
      while not q.empty():
         q.task_done()
         msg = q.get()
      LCD.setCursor(0,0)
      LCD.message(msg)
      q.task_done()
   return

# ----------------------------
# MAIN LOOP
# ----------------------------

def main():
   # Setup AdaFruit LCD Plate
   LCD.begin(16,2)
   LCD.clear()
   LCD.backlight(LCD.VIOLET)

   # Create the worker thread and make it a daemon
   worker = Thread(target=update_lcd, args=(LCD_QUEUE,))
   worker.setDaemon(True)
   worker.start()

   # Display startup banner
   display_ipaddr()
   LCD_QUEUE.put('Welcome to\nOpenExchanger', True)
   sleep(1)
   LCD.clear()

   # Main loop
   while True:
	lookup_btc()
	check_validator()
   update_lcd.join()

# ---------------------------------------
#  When seconds are just too much
# ---------------------------------------
def delay_milliseconds(milliseconds):
   seconds = milliseconds / float(1000)	# divide milliseconds by 1000 for seconds
   sleep(seconds)

# ----------------------------------------
# Retreive the current price of BTC in USD
# ----------------------------------------
def lookup_btc():
    #delay_milliseconds(99)
    url = 'https://blockchain.info/ticker'
    data = requests.get(url=url)
    binary = data.content
    output = simplejson.loads(binary)
    LCD_QUEUE.put('BTC Price: '+ str(output['USD']['buy']) + datetime.now().strftime('%b %d  %H:%M:%S\n'), True)

def check_validator():
	print wiringpi.digitalRead(VALIDATOR_PIN)

# ----------------------------
# DISPLAY TIME AND IP ADDRESS
# ----------------------------
def display_ipaddr():
   show_wlan0 = "ip addr show wlan0 | cut -d/ -f1 | awk '/inet/ {printf \"w%15.15s\", $2}'"
   show_eth0  = "ip addr show eth0  | cut -d/ -f1 | awk '/inet/ {printf \"e%15.15s\", $2}'"
   ipaddr = run_cmd(show_eth0)
   if ipaddr == "":
      ipaddr = run_cmd(show_wlan0)
   i = 29
   LCD_QUEUE.put(datetime.now().strftime('%b %d  %H:%M:%S\n')+ ipaddr, True)
   sleep(5)
   LCD.clear()

# ----------------------------
def run_cmd(cmd):  
   p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)  
   output = p.communicate()[0]  
   return output


if __name__ == '__main__':
  main()


