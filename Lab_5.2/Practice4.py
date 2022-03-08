import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) #GPIO24, #GPIO23, #GPIO22, #GPIO27
GPIO.setup (17, GPIO.IN) # GPIO 17 input
GPIO.setup (18, GPIO.OUT) # GPIO 18 output

#Blinking function
def blink(pin1):
    #setup GPIO output channel
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)

    GPIO.output(pin1, 1)
    time.sleep(0.3)
    GPIO.output(pin1, 0)
    time.sleep(0.3)
    GPIO.output(pin1, 1)
    time.sleep(0.3)
    GPIO.output(pin1, 0)
    time.sleep(0.3)
    GPIO.output(pin1, 1)
    time.sleep(0.3)
    GPIO.output(pin1, 0)
    time.sleep(0.3)

    GPIO.output(pin1, 0)
    time.sleep(0.1)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)
    GPIO.output(pin1, 1)
    time.sleep(0.1)
    GPIO.output(pin1, 0)
    time.sleep(0.1)



    

#main program blink #GPIO24, #GPIO23, #GPIO22, #GPIO27 infinity
try:
    while(1):
        if (GPIO.input (17)==0): #input low active
            time.sleep (0.3) # anti bouncing
            blink(18)
        else:
            GPIO.output (18, 0)
            time.sleep (0.3) # anti bouncing
            
except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")