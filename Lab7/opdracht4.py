#!/usr/bin/env python3 
import time
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


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
 	
# Load image and convert to 1 bit color.
#image = Image.open ('inmage.ppm').convert('1')
# Alternatively load a different format image, resize it, and convert to 1 bit color.
image = Image.open ('/home/pi/pi_scripts/Lab7/MaBoi.jpg').resize ( (display.width, display.height), Image.ANTIALIAS).convert ('1')

#Display image.
display.image (image)
display.show ()

