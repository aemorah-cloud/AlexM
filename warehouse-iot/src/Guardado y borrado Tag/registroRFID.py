#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pyrebase
import I2C_LCD_driver
import time

#Codigo para la pantalla
mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()

#Conexion a firebase
config = {     
  "apiKey": "PII",
  "authDomain": "PII",
  "databaseURL": "PII",
  "storageBucket": "PII"
}

mylcd.lcd_display_string("Inicializando ", 1, 0)
mylcd.lcd_display_string("Base de datos", 2, 0)
firebase = pyrebase.initialize_app(config)  
time.sleep(1.5)
mylcd.lcd_clear()
mylcd.lcd_display_string("Iniciada ", 2, 0)
mylcd.lcd_display_string("Base de datos", 1, 0)
time.sleep(1)
mylcd.lcd_clear()


reader = SimpleMFRC522()


try:
        database = firebase.database()
        mylcd.lcd_display_string("Ingrese la ", 1, 0)
        mylcd.lcd_display_string("Informacion", 2, 0)
        text = input('New data:')
        
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Ingrese el ", 1, 0)
        mylcd.lcd_display_string("TAG", 2, 0)
        print("Now place your tag to write")
        reader.write(text)
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Guardado", 1, 0)
        mylcd.lcd_display_string("Exitoso", 2, 0)
        print("Written")
        
        tagID,name = reader.read()
        #Guarda en la base de datos
        database.child('LectorRFID').child(tagID).set(name.strip())
        
finally:
        GPIO.cleanup()
