import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mfrc522
import time

reader = SimpleMFRC522()
while True: 
        try:
                
                status,TagType = reader.read_no_block()
                print(status)
                if status == None:
                        print('ossss')
                else:
                        print()
                        print('ok')
                        #id, text = reader.read()
                        #print(id)
                        #print(text)
                        #time.sleep(0.2)
                time.sleep(0.5)
        finally:
                GPIO.cleanup()
