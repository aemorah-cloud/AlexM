
import os
import RPi.GPIO as GPIO
import time

GPIO.cleanup()

# Se coloca el formato de los pines
GPIO.setmode(GPIO.BOARD)

# Pin del Buzzer
buzzer_pin = 15

# Pin para el seguro
actuator_pin = 13


GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(actuator_pin, GPIO.OUT)

GPIO.output(buzzer_pin, False)
GPIO.output(actuator_pin, True)
#GPIO.output(actuator_pin, False)
