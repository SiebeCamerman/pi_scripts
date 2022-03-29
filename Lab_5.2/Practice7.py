import RPi.GPIO as GPIO
import time

def blink(pin1, pin2, pin3, pin4):
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.setup(pin4, GPIO.OUT)
    GPIO.output(pin1, 1)
    time.sleep(0.01)
    GPIO.output(pin1, 0)
    GPIO.output(pin2, 1)
    time.sleep(0.01)
    GPIO.output(pin2, 0)
    GPIO.output(pin3, 1)
    time.sleep(0.01)
    GPIO.output(pin3, 0)
    GPIO.output(pin4, 1)
    time.sleep(0.01)
    GPIO.output(pin4, 0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
 

try:
    while (1):
        blink(22,23,24,27)



except KeyboardInterrupt:
    GPIO.cleanup()
    print("program executed")