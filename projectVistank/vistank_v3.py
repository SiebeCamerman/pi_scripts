# Project vistank
# Siebe Camerman
#----------------
# vistank v3
# 
# ultrasonic sensor

import RPi.GPIO as GPIO
import time
# setup in- and output
GPIO.setmode (GPIO.BCM)
GPIO.setup(18, GPIO.IN) # GPIO 18 input ultrasonic sensor
GPIO.setup(17, GPIO.OUT) # GPIO 17 output ultrasonic sensor

tankDepth = 30

#loop until ctrl^C
try:
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


except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")