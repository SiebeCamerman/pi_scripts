# Project vistank
# Siebe Camerman
#----------------
# vistank v1
# 
# relay's pump and light


import RPi.GPIO as GPIO
import time
# setup in- and output
GPIO.setmode (GPIO.BCM)
GPIO.setup (27, GPIO.IN) # GPIO 27 input pump
GPIO.setup (23, GPIO.IN) # GPIO 23 input light
GPIO.setup (24, GPIO.OUT) # GPIO 24 output pump
GPIO.setup (22, GPIO.OUT) # GPIO 22 output light

togglePump = 0
toggleLight = 0

alreadyPressed = 1


#loop until ctrl^C
try:
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


except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")
