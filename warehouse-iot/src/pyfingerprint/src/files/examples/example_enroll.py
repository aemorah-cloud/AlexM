#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""

import time
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2
import pyrebase
import I2C_LCD_driver


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


## Enrolls new finger
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

## Tries to enroll new finger
try:
    database = firebase.database()
    print('Waiting for finger...')
    mylcd.lcd_display_string("Ingrese el dedo ", 1, 0)

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(FINGERPRINT_CHARBUFFER1)

    ## Checks if finger is already enrolled
    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        mylcd.lcd_display_string("El dedo ya", 1, 0)
        mylcd.lcd_display_string("existe ", 2, 0)
        time.sleep(1)
        mylcd.lcd_clear()
        #exit(0)

    print('Remove finger...')
    time.sleep(2)

    print('Waiting for same finger again...')

    ## Wait that finger is read again
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 2
    f.convertImage(FINGERPRINT_CHARBUFFER2)

    ## Compares the charbuffers
    if ( f.compareCharacteristics() == 0 ):
        raise Exception('Fingers do not match')

    ## Creates a template
    f.createTemplate()

    ## Saves template at new position number
    nombre = input('Ingrese el nombre de la persona: ')
    cedula = input('Ingrese el numero de cedula de la persona: ')
    positionNumber = f.storeTemplate()
    
    info = { 'Nombre': nombre, 'Cedula': cedula}
    
    #Guarda en la base de datos
    database.child('SensorDactilar').child(positionNumber).set(info)
    
    
    print('Finger enrolled successfully!')
    mylcd.lcd_clear()
    mylcd.lcd_display_string("Guardado", 1, 0)
    mylcd.lcd_display_string("Exitoso", 2, 0)
    time.sleep(1)
    print('New template position #' + str(positionNumber))

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    #exit(1)
