import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)

ledStatus = True

while True:
    if (GPIO.input(4) == GPIO.LOW):
        print("button pressed!")
        time.sleep(0.3)
    time.sleep(0.01)