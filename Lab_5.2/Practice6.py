# event input /home/pi
import RPi.GPIO as GPIO
import time
# to use raspberry PI board GPIO numbers
GPIO.setmode (GPIO.BCM)
GPIO.setup (17, GPIO.IN) # GPIO 17 input
GPIO.setup (23, GPIO.IN) # GPIO 23 input
GPIO.setup (24, GPIO.OUT) # GPIO 24 output
GPIO.setup (22, GPIO.OUT) # GPIO 24 output


# loop forever or ctrl^C
try:
    while True:
        if (GPIO.input (23)==1): #input low active
            GPIO.output (22, 0)
            GPIO.output(24, 1)
            time.sleep (0.3) # anti bouncing
        elif (GPIO.input (17)==1):
            GPIO.output (24, 0)
            GPIO.output(22, 1)
            time.sleep (0.3) # anti bouncing
except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")