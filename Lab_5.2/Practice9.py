import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) #GPIO24, #GPIO23, #GPIO22, #GPIO27, #GPIO17
GPIO.setup (17, GPIO.IN) # GPIO 17 input

#Blinking function
def motorRechts(pin1,pin2,pin3,pin4):
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

def motorLinks(pin1,pin2,pin3,pin4):
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

#main program blink #GPIO24, #GPIO23, #GPIO22, #GPIO27 infinity
try:
    while(1):
        if (GPIO.input (17)==0): #input low active
            motorRechts(24,23,22,27)
            
        else:
            motorLinks(24,23,22,27)
            
        
except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")