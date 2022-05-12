# Project vistank
# Siebe Camerman
#----------------
# vistank v123
# 
# combi of pump,light, motor, ultrasonic sensor
# with adafruit IO and LCD

import cgitb ; cgitb.enable() 
import busio
import digitalio 
import board 

import threading
import RPi.GPIO as GPIO
import time

import adafruit_pcd8544 
from PIL import Image 
from PIL import ImageDraw 
from PIL import ImageFont

from Adafruit_IO import RequestError, Client, Feed

# setup for adafruit IO
ADAFRUIT_IO_USERNAME = "siebecamerman"
ADAFRUIT_IO_KEY = "aio_zXbD52Bip5sT5qS3E0mCocOGeWfF"

# read al the feeds
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
adafruit_waterDepth = aio.feeds('vistank.waterdepth')
adafruit_pumpState = aio.feeds('vistank.pumpstate')
adafruit_lightState = aio.feeds('vistank.lightstate')
adafruit_lightOn = aio.feeds('vistank.lighton')
adafruit_lightOff = aio.feeds('vistank.lightoff')
adafruit_feedOn = aio.feeds('vistank.feedon')

# setup in- and output
GPIO.setmode (GPIO.BCM)
GPIO.setup (27, GPIO.IN) # GPIO 27 input pump
GPIO.setup (26, GPIO.IN) # GPIO 26 input light
GPIO.setup (16, GPIO.OUT) # GPIO 16 output pump
GPIO.setup (22, GPIO.OUT) # GPIO 22 output light
GPIO.setup (25, GPIO.IN) # GPIO 25 input step motor
GPIO.setup(18, GPIO.IN) # GPIO 18 input ultrasonic sensor
GPIO.setup(17, GPIO.OUT) # GPIO 17 output ultrasonic sensor

GPIO.output (16,1)
GPIO.output (22,1)

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

# Get drawing object to draw on image
image = Image.new('1', (display.width, display.height)) 
draw = ImageDraw.Draw(image)
 	
# Draw a white filled box to clear the image.
draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)



tankDepth = 25                      # This is the height of the fishtank in centimeters
waterHeight = 16                    # The height of the water level in centimeters
lightOn = "13:23:00"                # When the light needs to turn on every day
lightOff = "13:23:10"               # When the light needs to turn off every day

feedOn = "13:23:30"                 # When you want to feed the fish every day

lightState = 0
pumpState = 0
waterDepth = 0

delay_send_date = 6


def pumpLight():                    # Function that controls the light
    toggleLight = 0
    timer = 0
    global lightState

    alreadyPressed = 1
    current_time = ""
    while True:
        #relay's
        current_time = time.strftime("%H:%M:%S", time.localtime())      # Get the time in format hh:mm:ss
        if (current_time == lightOn and timer == 0):                    # When its time to put the light on and the light isn't on:
            timer = 1
            lightState = 1
            GPIO.output (22, 0)                                         # We turn on the light
            
        elif (current_time == lightOff and timer == 1):                 # When its time to put the light off and the light is on:
            timer = 0
            lightState = 0
            GPIO.output (22, 1)                                         # We turn off the light
            


        if (GPIO.input (26)==0): #input low active
            if (toggleLight == 1 and alreadyPressed == 1 and timer == 0):   #When you press the button and the light is on and the light isn't turn on by the timer
                alreadyPressed = 0
                toggleLight = 0
                lightState = 0
                GPIO.output (22, 1)                                         # We turn off the light
                time.sleep (0.3) # anti bouncing
            elif (toggleLight == 0 and alreadyPressed == 1 and timer == 0): #When you press the button and the light is off and the light isn't turn on by the timer
                alreadyPressed = 0
                toggleLight = 1
                lightState = 1
                GPIO.output(22, 0)                                          # We turn on the light
                time.sleep (0.3) # anti bouncing
        else:
            alreadyPressed = 1                  # With this variable I make sure that the light doesn't keep going on and off when you keep pressing the button                                         

        print("LightState",lightState)
        time.sleep(0.1)

def motorRechts():                          # Function that turns the motor to the right
    pin1 = 21
    pin2 = 9
    pin3 = 5
    pin4 = 6
    #setup GPIO output channel
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.output(pin1, 1)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.output(pin2, 1)
    time.sleep(0.01)
    GPIO.output(pin1, 0)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.output(pin3, 1)
    time.sleep(0.01)
    GPIO.output(pin2, 0)
    GPIO.setup(pin4, GPIO.OUT)
    GPIO.output(pin4, 1)
    time.sleep(0.01)
    GPIO.output(pin3, 0)
    GPIO.output(pin1, 1)
    time.sleep(0.01)
    GPIO.output(pin4, 0)

def motorLinks():                          # # Function that turns the motor to the left
    pin1 = 21
    pin2 = 9
    pin3 = 5
    pin4 = 6
    #setup GPIO output channel
    GPIO.setup(pin4, GPIO.OUT)
    GPIO.output(pin4, 1)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.output(pin3, 1)
    time.sleep(0.01)
    GPIO.output(pin4, 0)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.output(pin2, 1)
    time.sleep(0.01)
    GPIO.output(pin3, 0)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.output(pin1, 1)
    time.sleep(0.01)
    GPIO.output(pin2, 0)
    GPIO.output(pin4, 1)
    time.sleep(0.01)
    GPIO.output(pin1, 0)  


def stepMotor():                                                        # Function for the feeder
    enableFeed = 0
    counter = 0
    while(True):
        current_time = time.strftime("%H:%M:%S", time.localtime())      # Get the time in format hh:mm:ss
        if (current_time == feedOn):                                    # When its time to feed we are setting the variable on 1
            enableFeed = 1
            counter = 0


        if (GPIO.input (25)==0 or enableFeed == 1): #input low active   # when the button is pressed or its time to feed
            motorLinks()                                                # We are gonna spin the motor
            if (enableFeed == 1):                                       # When the motor is enabled by the timer we are gonna spin until it makes a full turn
                counter += 1
            if (counter == 505):
                enableFeed = 0

def ultrasonicSensor():                                                 # Function that meassures the waterDepth and turn on the pump
    global waterDepth
    togglePump = 0
    global pumpState
    toggleSensor = 0

    firstTime = 0
    secondTime = 0
    counter = 0


    while True:
        #ultrasonic sensor meassurement
        GPIO.output(17, 1)
        time.sleep(0.00001)
        GPIO.output(17, 0)

        while(GPIO.input(18) == 0):
            pass

        signalHigh = time.time()

        while(GPIO.input(18) == 1):
            pass

        signalLow = time.time()
        timePassed = signalLow - signalHigh
        distance = 17000 * timePassed
        print("Waterdiepte in cm: "+str(tankDepth-distance))
        waterDepth = tankDepth-distance                             # Calculate the waterDepth
        time.sleep(0.1)


        if ((tankDepth-distance)< waterHeight and togglePump == 0): # When the waterDepth is too low and the pump is off
            if(secondTime == 1 and counter == 1):                   # we check 3 times in a row if the water is too low  to prevent the pump from starting immediately in the event of an incorrect measurement
                toggleSensor = 1
                GPIO.output (16, 0)                                 # When we are sure its too low we start the pump
                pumpState = 1
                firstTime = 0
                secondTime = 0
            if(firstTime == 1):
                secondTime = 1
            firstTime = 1
            counter = 0
        counter += 1
        if ((tankDepth-distance)> waterHeight + 1 and toggleSensor == 1):   #When the pump is running we check when the waterDept is high enough
            toggleSensor = 0
            GPIO.output (16, 1)                                                # We turn off the pump
            pumpState = 0
            firstTime = 0
            secondTime = 0
        if (GPIO.input (27)==0 and toggleSensor == 0): #input low active       #When we hold the button and the pump is not activated by the sensor
            togglePump = 1          
            GPIO.output (16, 0)                                                # We turn on the pump
            pumpState = 1
            time.sleep (0.3) # anti bouncing
        if (GPIO.input (27)==1 and togglePump == 1):                           # When we release the button and the pump is running 
            togglePump = 0
            GPIO.output(16, 1)                                                 # We turn off the pump
            pumpState = 0
            time.sleep (0.3) # anti bouncing
        print("PumpState:",pumpState) 

def LCD():                                                              # Function where we show info on the LCD                                                        

    logo = Image.open ('/home/pi/pi_scripts/projectVistank/fish.PNG').resize ( (display.width, display.height), Image.ANTIALIAS).convert ('1')      # Fish logo

    while True:
        # Draw a white filled box to clear the image. 
        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

        # Write current Time, current waterDepth
        draw.text((1,0), str(time.strftime("%H:%M:%S", time.localtime())), font=font) 
        draw.text((1,8), 'Current', font=font)
        draw.text((1,16), 'Waterdepth ', font=font)
        draw.text((1,32), (str(waterDepth)), font=font) 
        display.image(image)
        display.show()
        time.sleep(2)

        # Draw a white filled box to clear the image. 
        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

        # Write current time, Light state and Pump state
        draw.text((1,0), str(time.strftime("%H:%M:%S", time.localtime())), font=font) 
        draw.text((1,8), ('Light State'), font=font) 
        draw.text((1,16), (str(lightState)), font=font) 
        draw.text((1,24), ('Pump State'), font=font) 
        draw.text((1,32), (str(pumpState)), font=font)
        display.image(image)
        display.show()
        time.sleep(2)

        # Draw a white filled box to clear the image. 
        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

        # Write the current time, when the light will turn on and off
        draw.text((1,0), str(time.strftime("%H:%M:%S", time.localtime())), font=font) 
        draw.text((1,8), ('Light On'), font=font) 
        draw.text((1,16), (str(lightOn)), font=font)
        draw.text((1,24), ('Light Off' ), font=font) 
        draw.text((1,32), (str(lightOff)), font=font)
        display.image(image)
        display.show()
        time.sleep(2)

        # Draw a white filled box to clear the image. 
        draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

        # Write the current time, when the next feeding is
        draw.text((1,0), str(time.strftime("%H:%M:%S", time.localtime())), font=font) 
        draw.text((1,8), ('Next feeding'), font=font) 
        draw.text((1,16), (str(feedOn)), font=font)
        display.image(image)
        display.show()
        time.sleep(2)

        #Display the fish logo
        display.image (logo) 
        display.show ()
        time.sleep(2)


#create 4 new threads
tpumpLight = threading.Thread(target=pumpLight)                     # Thread that controls the light
tstepMotor = threading.Thread(target=stepMotor)                     # Thread for the feeder
tultrasonicSensor = threading.Thread(target=ultrasonicSensor)       # Thread that meassures the waterDepth and turn on the pump
tlcd = threading.Thread(target=LCD)                                 # Thread where we show info on the LCD  

#start the threads
tpumpLight.start()
tstepMotor.start()
tultrasonicSensor.start()
tlcd.start()

#loop until ctrl^C
try:
    while True:
        #Read data on adafruit IO
        changedLightOn = aio.receive("vistank.lighton").value   
        changedLightOff = aio.receive("vistank.lightoff").value
        changedFeedOn = aio.receive("vistank.feedon").value
        current_time = time.strftime("%H:%M", time.localtime())
        #Send data to adafruit IO
        #For free users you can only send 30 request per minute thats why i have 6 seconds delay
        delay_send_date = 6
        aio.send_data(adafruit_waterDepth.key, waterDepth)
        aio.send_data(adafruit_pumpState.key, pumpState)
        aio.send_data(adafruit_lightState.key, lightState)
        if (lightOn != changedLightOn or lightOff != changedLightOff or feedOn != changedFeedOn): #If time changed on adafruit IO we are gonna update in our program
            lightOn = changedLightOn
            lightOff = changedLightOff
            feedOn = changedFeedOn
            aio.send_data(adafruit_lightOn.key, lightOn)
            aio.send_data(adafruit_lightOff.key, lightOff)
            aio.send_data(adafruit_feedOn.key, feedOn)
            #Because we need to send more data I update the delay
            delay_send_date = 12
        time.sleep(delay_send_date)

        


except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")
