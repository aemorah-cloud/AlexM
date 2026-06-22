import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
delayt = .1 
value = 0 # this variable will be used to store the ldr value
ldr = 18 #ldr is connected with pin number 7
led = 11 #led is connected with pin number 11

GPIO.setup(led, GPIO.OUT) # as led is an output device so that’s why we set it to output.
GPIO.output(led, False) # keep led off by default 

GPIO.setup(ldr, GPIO.IN)


contador = 0
enable = True
try:
    # Main loop
    while True:
        #print("Ldr Value:")
        if (GPIO.input(ldr) != 0 and enable == True):
            contador+=1
            enable = False
            time.sleep(0.5)
            print(contador)
        if (GPIO.input(ldr) == 0):
            enable = True
            
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
