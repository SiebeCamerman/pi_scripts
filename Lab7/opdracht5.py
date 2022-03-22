#!/usr/bin/env python3 
import time
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from adafruit_bus_device.spi_device import SPIDevice

from mpd import MPDClient
# event input /home/pi
import RPi.GPIO as GPIO
# to use raspberry PI board GPIO numbers
GPIO.setmode (GPIO.BCM)
GPIO.setup (17, GPIO.IN) # GPIO 17 input
GPIO.setup (4, GPIO.IN) # GPIO 4 output

# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize display
dc = digitalio.DigitalInOut(board.D23)  # data/command
cs1 = digitalio.DigitalInOut(board.CE1)  # chip select CE1 for display
reset = digitalio.DigitalInOut(board.D24)  # reset
display = adafruit_pcd8544.PCD8544(spi, dc, cs1, reset, baudrate= 1000000)
display.bias = 4
display.contrast = 60
display.invert = True

#  Clear the display.  Always call show after changing pixels to make the display update visible!
display.fill(0)
display.show()

# Load default font.
font = ImageFont.load_default()
#font=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 10)

# Get drawing object to draw on image
image = Image.new('1', (display.width, display.height)) 
draw = ImageDraw.Draw(image)
 	

client = MPDClient()               	# create client object
client.timeout = 10                	# network timeout in seconds
client.idletimeout = None    
client.connect("localhost", 6600)  	# connect to localhost:6600
print(client.mpd_version)          	# print the MPD version

client.play

# loop forever or ctrl^C
try:
    while True:
        if (GPIO.input (17)==0): #input low active
            print ("next station")
            #client.command_list_ok_begin()
            client.next()
            # Draw a white filled box to clear the image.
            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

            result = 'mnm' 

            # Write some text.
            draw.text((1,0), result, font=font)
            display.image(image)
            display.show()
            print(result)
            time.sleep (0.3) # anti bouncing
        elif (GPIO.input (4)==0):
            print ("prev. station")
            client.previous()
            # Draw a white filled box to clear the image.
            draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
            result = 'stubru'
            # Write some text.
            draw.text((1,0), result, font=font)
            display.image(image)
            display.show()
            print(result)
            time.sleep (0.3) # anti bouncing
except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    client.close()                     	# send the close command
    client.disconnect()                	# disconnect from the server
    print("clean closed")



