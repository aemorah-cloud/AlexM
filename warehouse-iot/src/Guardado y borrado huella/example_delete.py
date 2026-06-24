#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""

from pyfingerprint.pyfingerprint import PyFingerprint
import pyrebase
import I2C_LCD_driver
import time


#Codigo para la pantalla
mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()

#Conexion a firebase
config = {     
  "apiKey": "AIzaSyAzUt1jt8hZwM-jeUbigoQwDJmGv7nb2lA",
  "authDomain": "tesis-mora-moran.firebaseapp.com",
  "databaseURL": "https://tesis-mora-moran-default-rtdb.firebaseio.com",
  "storageBucket": "tesis-mora-moran.appspot.com"
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



## Deletes a finger from sensor
##


## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    mylcd.lcd_display_string("No se inicializo", 1, 0)
    mylcd.lcd_display_string("el sensor ", 2, 0)
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to delete the template of the finger
try:
    database = firebase.database()
    mylcd.lcd_display_string("Siga las instrucciones", 1, 0)
    mylcd.lcd_display_string("en consola", 2, 0)
    positionNumber = input('Please enter the template position you want to delete: ')
    positionNumber = int(positionNumber)
    

    if ( f.deleteTemplate(positionNumber) == True ):
        database.child('SensorDactilar').child(positionNumber).remove()
        print('Template deleted!')
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Borrado ", 1, 0)
        mylcd.lcd_display_string("Exitoso ", 2, 0)

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
