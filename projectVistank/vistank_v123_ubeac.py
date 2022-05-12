# Project vistank
# Siebe Camerman
#----------------
# vistank v123
# 
# combi of pump,light, motor, ultrasonic sensor
# with ubeac

import cgitb ; cgitb.enable() 
import spidev 
import busio
import digitalio 
import board 
import requests 
from adafruit_bus_device.spi_device import SPIDevice 
url = "http://raspsiepi.hub.ubeac.io/iotesssiebecamerman" 
uid = "iotess siebecamerman"

import threading
import RPi.GPIO as GPIO
import time
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

tankDepth = 25
waterHeight = 11
lightOn = "16:25:00"
lightOff = "16:26:10"

feedOn = "16:17:00"



def pumpLight():
    toggleLight = 0
    lightState = 0
    timer = 0

    alreadyPressed = 1
    current_time = ""
    while True:
        #relay's
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if (current_time == lightOn and timer == 0):
            timer = 1
            lightState = 1
            GPIO.output (22, 0)
            
        elif (current_time == lightOff and timer == 1):
            timer = 0
            lightState = 0
            GPIO.output (22, 1)
            


        if (GPIO.input (26)==0): #input low active
            if (toggleLight == 1 and alreadyPressed == 1 and timer == 0):
                alreadyPressed = 0
                toggleLight = 0
                lightState = 0
                GPIO.output (22, 1)
                time.sleep (0.3) # anti bouncing
            elif (toggleLight == 0 and alreadyPressed == 1 and timer == 0):
                alreadyPressed = 0
                toggleLight = 1
                lightState = 1
                GPIO.output(22, 0)
                time.sleep (0.3) # anti bouncing
        else:
            alreadyPressed = 1


        tmLightState = (lightState)
        data= { 
            "id": uid, 
            "sensors":[{ 
                'id': 'light', 
                'data': tmLightState 
                }] 
        } 
        print("LightState",lightState)
        r = requests.post(url, verify=False, json=data)

def motorRechts():
    pin1 = 8
    pin2 = 9
    pin3 = 10
    pin4 = 11
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

def motorLinks():
    pin1 = 8
    pin2 = 9
    pin3 = 10
    pin4 = 11
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


def stepMotor():
    enableFeed = 0
    counter = 0
    while(True):
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if (current_time == feedOn):
            enableFeed = 1
            counter = 0


        if (GPIO.input (25)==0 or enableFeed == 1): #input low active
            motorLinks()
            if (enableFeed == 1):
                counter += 1
            if (counter == 500):
                enableFeed = 0

def ultrasonicSensor():
    togglePump = 0
    pumpState = 0
    toggleSensor = 0

    firstTime = 0
    secondTime = 0
    counter = 0

    while True:
        #ultrasonic sensor
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
        time.sleep(0.1)


        if ((tankDepth-distance)< waterHeight and togglePump == 0):
            if(secondTime == 1 and counter == 1):
                toggleSensor = 1
                GPIO.output (16, 0)
                pumpState = 1
                firstTime = 0
                secondTime = 0
            if(firstTime == 1):
                secondTime = 1
            firstTime = 1
            counter = 0
        counter += 1
        if ((tankDepth-distance)> waterHeight + 1 and toggleSensor == 1):
            toggleSensor = 0
            GPIO.output (16, 1)
            pumpState = 0
            firstTime = 0
            secondTime = 0
        if (GPIO.input (27)==0 and toggleSensor == 0): #input low active
            togglePump = 1
            GPIO.output (16, 0)
            pumpState = 1
            time.sleep (0.3) # anti bouncing
        if (GPIO.input (27)==1 and togglePump == 1):
            togglePump = 0
            GPIO.output(16, 1)
            pumpState = 0
            time.sleep (0.3) # anti bouncing
        print("PumpState:",pumpState)
        tmUltrasonicSensor = (tankDepth-distance)
        tmPumpState = (pumpState)
        data= { 
            "id": uid, 
            "sensors":[{ 
                'id': 'ultrasonic sensor', 
                'data': tmUltrasonicSensor 
                }, 
                {'id': 'pump', 
                'data': tmPumpState 
                }] 
        } 
        r = requests.post(url, verify=False, json=data)
        

#create two new threads
tpumpLight = threading.Thread(target=pumpLight)
tstepMotor = threading.Thread(target=stepMotor)
tultrasonicSensor = threading.Thread(target=ultrasonicSensor)

#start the threads
tpumpLight.start()
tstepMotor.start()
tultrasonicSensor.start()

#loop until ctrl^C
try:
    while True:
        tmLightOn = (lightOn)
        tmLightOff = (lightOff)
        tmfeedOn = (feedOn)
        data= { 
            "id": uid, 
            "sensors":[{ 
                'id': 'lightOn', 
                'data': tmLightOn 
                }, 
                {'id': 'lightOff', 
                'data': tmLightOff 
                }, 
                {'id': 'feedOn', 
                'data': tmfeedOn
                }] 
        } 
        r = requests.post(url, verify=False, json=data)
        print('JAAAAAAAH')
        time.sleep(5)


except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")
