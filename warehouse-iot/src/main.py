#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import RPi.GPIO as GPIO
import time
from datetime import datetime
from picamera import PiCamera
import smtplib
import hashlib
import I2C_LCD_driver
#from pyfingerprint//src//files//pyfingerprint//pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
import pyrebase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mfrc522 import SimpleMFRC522
import mfrc522

GPIO.cleanup()

# Se coloca el formato de los pines
GPIO.setmode(GPIO.BOARD)

# Pin para el boton
button_pin = 7

# Pin para el LED
led_pin = 11

# Pin para el seguro
actuator_pin = 13

# Pin del Buzzer
buzzer_pin = 15

#Pin para el LDR
ldr = 18 

# Pines del Motor
StepPinForward=29
StepPinBackward= 31
sleeptime=1

#Se inicializa el LED
mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()
dimLCD = " " * 16


#Se define el lector de Huella
reader = SimpleMFRC522()



# Set the button, LED, and actuator as inputs and outputs
GPIO.setup(button_pin, GPIO.IN)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(actuator_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(StepPinForward, GPIO.OUT)
GPIO.setup(StepPinBackward, GPIO.OUT)
GPIO.setup(ldr, GPIO.IN)


## Se inicializa el sensor dactilar
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Informacion del sensor
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))



# Informacion para envio de correo
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "raspberrypi.mora.moran@gmail.com"
SMTP_PASSWORD = "mpfyyqsmcihqgqfw"
EMAIL_TO = "aemorah@gmail.com"
EMAIL_SUBJECT = "Ingreso irregular en la bodega "


#Informacion para la base de datos
config = {     
  "apiKey": "AIzaSyAzUt1jt8hZwM-jeUbigoQwDJmGv7nb2lA",
  "authDomain": "tesis-mora-moran.firebaseapp.com",
  "databaseURL": "https://tesis-mora-moran-default-rtdb.firebaseio.com",
  "storageBucket": "tesis-mora-moran.appspot.com"
}

#Se inicializa la base de datos
mylcd.lcd_display_string("Inicializando ", 1, 0)
mylcd.lcd_display_string("Base de datos", 2, 0)
firebase = pyrebase.initialize_app(config)
time.sleep(1.5)
mylcd.lcd_clear()
mylcd.lcd_display_string("Iniciada ", 2, 0)
mylcd.lcd_display_string("Base de datos", 1, 0)
time.sleep(1)
mylcd.lcd_clear()

# Se coloca en estado inicial los actuadores
GPIO.output(led_pin, False)
GPIO.output(actuator_pin, True)


# Funcion para el conteo de personas
contador = 0
enable = True

# Create a PiCamera object
camera = PiCamera()


# Funcion para la toma de imagen
def take_picture(usuario, baseDatos):
  storage = firebase.storage()
  # Formato en la que se guardara
  now  = datetime.now()
  formatoImagen = now.strftime('%d%m%Y%H:%M:%S')
  formatoBase = now.strftime('%d%m%Y')
  formatoClave = now.strftime('%H:%M:%S')
  name = formatoImagen+'.jpg'
  nombreArchivo = name
  camera.capture(name)
  mylcd.lcd_display_string('Foto tomada', 1, 0)
  time.sleep(1)
  mylcd.lcd_clear()
  baseDatos.child('EntradaPuerta').child(formatoBase).child(usuario).child(formatoClave).set(name)
  storage.child(name).put(name)
  mylcd.lcd_display_string('Foto enviada', 1, 0)
  time.sleep(1)
  mylcd.lcd_clear()
  return nombreArchivo
  

#Funcion para mover el motor en un sentido
def forward(x):
    GPIO.output(StepPinForward, GPIO.HIGH)
    print ("forwarding running  motor ")
    time.sleep(x)
    GPIO.output(StepPinForward, GPIO.LOW)
    
#Funcion para mover el motor en otro sentido
def reverse(x):
    GPIO.output(StepPinBackward, GPIO.HIGH)
    print ("backwarding running motor")
    time.sleep(x)
    GPIO.output(StepPinBackward, GPIO.LOW)

#Funcion para manda correo
def send_email(subject, body,nombreArchivo):
    """
    Send an email
    """
    with open(nombreArchivo, 'rb') as f:
        img_data = f.read()
        
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = EMAIL_TO
    text = MIMEText(body)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(nombreArchivo))
    msg.attach(image)

    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(SMTP_USERNAME, SMTP_PASSWORD)
    s.sendmail(SMTP_USERNAME, EMAIL_TO, msg.as_string())
    s.quit()
    
    mylcd.lcd_display_string('Mensaje enviado', 1, 0)
    mylcd.lcd_display_string('exitosamente', 2, 0)
    print('mensaje enviado exitosamente')
    time.sleep(1)
    mylcd.lcd_clear()



# Main loop
while True:
  try:
    print('Waiting for finger...')
    mylcd.lcd_display_string('Escanee Dedo o', 1, 0)
    mylcd.lcd_display_string('Ingrese tarjeta', 2, 0)
    status,TagType = reader.read_no_block()
    
    ## Esperando la lectura del dedod
    while True:
        status,TagType = reader.read_no_block()
        database = firebase.database()
        if f.readImage() == True:
            mylcd.lcd_clear()
            mylcd.lcd_display_string('Escaneando Huella', 1, 0)
            
            ## Convierte la imagen leida y la guarda
            f.convertImage(FINGERPRINT_CHARBUFFER1)
            
            ## busca el modelo
            result = f.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]
            
            #Codigo del sensor dactilar
            if ( positionNumber == -1 ):
                print('No se encontro la imagen!')
                mylcd.lcd_display_string('No se encontro', 1, 0)
                mylcd.lcd_display_string('la imagen', 2, 0)
                time.sleep(1)
                mylcd.lcd_clear()
                
            else:
                nombre = database.child("SensorDactilar").child(positionNumber).child('Nombre').get().val()
                print('Found template at position #' + str(positionNumber))
                print('The accuracy score is: ' + str(accuracyScore))
                mylcd.lcd_clear()
                mylcd.lcd_display_string('Bienvenido', 1, 0)
                mylcd.lcd_display_string(nombre, 2, 0)
                
                GPIO.output(led_pin, True)
                GPIO.output(buzzer_pin, GPIO.HIGH)
                GPIO.output(actuator_pin, False)
                time.sleep(2)
                print ("forward motor ")
                forward(4)
                time.sleep(1)
                GPIO.output(led_pin, False)
                GPIO.output(buzzer_pin, GPIO.LOW)
                print('Foto tomada')
                nombreFoto = take_picture(nombre,database)

                tiempoIni = time.perf_counter()
                while True:
                    #print(GPIO.input(button_pin))
                    timpoNow = time.perf_counter()
                    if (GPIO.input(ldr) != 0 and enable == True):
                        contador+=1
                        enable = False
                        time.sleep(0.5)
                        print(contador)
                    if (GPIO.input(ldr) == 0):
                        enable = True
                    
                    if(GPIO.input(button_pin)):
                        GPIO.output(led_pin, True)
                        GPIO.output(buzzer_pin, GPIO.HIGH)
                        print ("reverse motor")
                        reverse(4)
                        GPIO.output(actuator_pin, True)
                        GPIO.output(led_pin, False)
                        GPIO.output(buzzer_pin, GPIO.LOW)
                        break

                    if timpoNow - tiempoIni > 30:
                        GPIO.output(led_pin, True)
                        GPIO.output(buzzer_pin, GPIO.HIGH)
                        print("reverse motor")
                        reverse(4)
                        GPIO.output(actuator_pin, True)
                        GPIO.output(led_pin, False)
                        GPIO.output(buzzer_pin, GPIO.LOW)
                        break
                    
                    
                if (contador > 1):
                    #Sent email
                    bodyMensaje = "Existe un ingreso irregular en la bodega \n Nombre: "+ nombre+ "\n Favor revisar la base de datos."
                    send_email(EMAIL_SUBJECT, bodyMensaje,nombreFoto)
                    time.sleep(0.2)
                time.sleep(1)
                os.remove(nombreFoto)
            contador = 0
            break
            
        elif status != None:
            mylcd.lcd_clear()
            mylcd.lcd_display_string('Escaneando Tarjeta', 1, 0)
            time.sleep(1)
            print('tarjeta leida')
            time.sleep(1)
            mylcd.lcd_clear()
            mylcd.lcd_display_string('Bienvenido', 1, 0)
            mylcd.lcd_display_string(TagType, 2, 0)
            
            GPIO.output(led_pin, True)
            GPIO.output(buzzer_pin, GPIO.HIGH)
            GPIO.output(actuator_pin, False)
            time.sleep(2)
            print ("forward motor ")
            forward(4)
            time.sleep(1)
            GPIO.output(led_pin, False)
            GPIO.output(buzzer_pin, GPIO.LOW)
            print('Foto tomada')
            nombreFoto = take_picture(TagType,database)

            tiempoIni = time.perf_counter()
            while True:
                #print(GPIO.input(button_pin))
                timpoNow = time.perf_counter()
                if (GPIO.input(ldr) != 0 and enable == True):
                    contador+=1
                    enable = False
                    time.sleep(0.5)
                    print(contador)
                if (GPIO.input(ldr) == 0):
                    enable = True
                
                if(GPIO.input(button_pin)):
                    GPIO.output(led_pin, True)
                    GPIO.output(buzzer_pin, GPIO.HIGH)
                    print ("reverse motor")
                    reverse(4)
                    GPIO.output(actuator_pin, True)
                    GPIO.output(led_pin, False)
                    GPIO.output(buzzer_pin, GPIO.LOW)
                    break

                if timpoNow - tiempoIni > 30:
                    GPIO.output(led_pin, True)
                    GPIO.output(buzzer_pin, GPIO.HIGH)
                    print("reverse motor")
                    reverse(4)
                    GPIO.output(actuator_pin, True)
                    GPIO.output(led_pin, False)
                    GPIO.output(buzzer_pin, GPIO.LOW)
                    break
                
                
                
                
            if (contador > 1):
                #Sent email
                bodyMensaje = "Existe un ingreso irregular en la bodega \n Nombre: "+ nombre+ "\n Favor revisar la base de datos."
                send_email(EMAIL_SUBJECT, bodyMensaje,nombreFoto)
                time.sleep(0.2)
            time.sleep(1)
            os.remove(nombreFoto)
            contador = 0
            break

        start_time = time.perf_counter()
        if (GPIO.input(button_pin)):
            GPIO.output(led_pin, True)
            GPIO.output(buzzer_pin, GPIO.HIGH)
            GPIO.output(actuator_pin, False)
            time.sleep(2)
            print("forward motor ")
            forward(4)
            time.sleep(1)
            GPIO.output(led_pin, False)
            GPIO.output(buzzer_pin, GPIO.LOW)
            
            while True:
                if GPIO.input(ldr) != 0:
                    GPIO.output(led_pin, True)
                    GPIO.output(buzzer_pin, GPIO.HIGH)
                    print("reverse motor")
                    reverse(4)
                    GPIO.output(actuator_pin, True)
                    GPIO.output(led_pin, False)
                    GPIO.output(buzzer_pin, GPIO.LOW)
                    break
                
            
            
            

  except Exception as e:
    print('Operation failed!')
    mylcd.lcd_display_string('No se encontro  ', 1, 0)
    mylcd.lcd_display_string('registro...', 2, 0)
    time.sleep(2)
    mylcd.lcd_clear()
    print('Exception message: ' + str(e))
    #exit(1)
    
  # Wait for a moment
  time.sleep(0.1)
