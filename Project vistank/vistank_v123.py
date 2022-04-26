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



def pumpLight():
    #togglePump = 0
    toggleLight = 0

    alreadyPressed = 1
    while True:
        #relay's
        
        if (GPIO.input (27)==1): #input low active
            GPIO.output (24, 1)
            time.sleep (0.3) # anti bouncing
        else:
            GPIO.output(24, 0)
            time.sleep (0.3) # anti bouncing

        if (GPIO.input (23)==0): #input low active
            if (toggleLight == 1 and alreadyPressed == 1):
                alreadyPressed = 0
                toggleLight = 0
                GPIO.output (22, 1)
                time.sleep (0.3) # anti bouncing
            elif (toggleLight == 0 and alreadyPressed == 1):
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

def stepMotor():
    while(True):
        if (GPIO.input (25)==0): #input low active
            motorRechts()

#create two new threads
tpumpLight = threading.Thread(target=pumpLight)
tstepMotor = threading.Thread(target=stepMotor)

#start the threads
tpumpLight.start()
tstepMotor.start()

#loop until ctrl^C
try:
    while True:
        print('Still working')
        time.sleep(5)


except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")
