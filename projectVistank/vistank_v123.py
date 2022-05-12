# Project vistank
# Siebe Camerman
#----------------
# vistank v123
# 
# combi of pump,light, motor, ultrasonic sensor


import threading
import RPi.GPIO as GPIO
import time
# setup in- and output
GPIO.setmode (GPIO.BCM)
GPIO.setup (27, GPIO.IN) # GPIO 27 input pump
GPIO.setup (23, GPIO.IN) # GPIO 23 input light
GPIO.setup (24, GPIO.OUT) # GPIO 24 output pump
GPIO.setup (22, GPIO.OUT) # GPIO 22 output light
GPIO.setup (25, GPIO.IN) # GPIO 25 input step motor
GPIO.setup(18, GPIO.IN) # GPIO 18 input ultrasonic sensor
GPIO.setup(17, GPIO.OUT) # GPIO 17 output ultrasonic sensor

GPIO.output (24,1)
GPIO.output (22,1)

tankDepth = 25
waterHeight = 13
lightOn = "17:22:00"
lightOff = "17:22:10"

feedOn = "20:45:20"



def pumpLight():
    toggleLight = 0
    timer = 0

    alreadyPressed = 1
    current_time = ""
    while True:
        #relay's
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if (current_time == lightOn and timer == 0):
            timer = 1
            print("ja")
            GPIO.output (22, 0)
        elif (current_time == lightOff and timer == 1):
            timer = 0
            GPIO.output (22, 1)
        
        #if (current_time == "23" and timer == 0):
        #    timer = 1
        #    GPIO.output (22, 0)
        #if (current_time == "24" and timer == 1):
        #    time = 0
        #    GPIO.output (22, 1)
        #print(current_time)

        if (GPIO.input (23)==0): #input low active
            if (toggleLight == 1 and alreadyPressed == 1 and timer == 0):
                alreadyPressed = 0
                toggleLight = 0
                GPIO.output (22, 1)
                print('aan')
                time.sleep (0.3) # anti bouncing
            elif (toggleLight == 0 and alreadyPressed == 1 and timer == 0):
                alreadyPressed = 0
                toggleLight = 1
                GPIO.output(22, 0)
                time.sleep (0.3) # anti bouncing
        else:
            alreadyPressed = 1

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
    toggleSensor = 0

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
        time.sleep(1)

        if ((tankDepth-distance)< waterHeight and togglePump == 0):
            toggleSensor = 1
            GPIO.output (24, 0)
        if ((tankDepth-distance)> waterHeight + 1 and toggleSensor == 1):
            toggleSensor = 0
            GPIO.output (24, 1)

        if (GPIO.input (27)==0 and toggleSensor == 0): #input low active
            togglePump = 1
            GPIO.output (24, 0)
            time.sleep (0.3) # anti bouncing
        if (GPIO.input (27)==1 and togglePump == 1):
            togglePump = 0
            GPIO.output(24, 1)
            time.sleep (0.3) # anti bouncing

        

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
        print('JAAAHHHH')
        time.sleep(5)


except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")
