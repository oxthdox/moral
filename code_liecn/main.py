# encoding: utf-8
# !/usr/bin/env python
# This is a demo for security#encoding: utf-8
#!/usr/bin/env python
#This is a demo for security door. For more details, you can consult readme.docx

import os
import speech_recognition as sr
import wave
import time
import cognitive_face as CF
import sys
from PIL import Image
import threading
import RPi.GPIO as GPIO
import struct
import sys
import pigpio
import json
from watson_developer_cloud import VisualRecognitionV3

#pin: the GPIO pin you choose
#times: times to blink
#delay: duration between blinking
def light(pin, times, delay):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin,GPIO.OUT)
	onoff = GPIO.LOW
	
	i = 0
	while i < times:
		if onoff == GPIO.LOW:
			onoff = GPIO.HIGH
		else:
			onoff = GPIO.LOW
		GPIO.output(pin, onoff)
		time.sleep(delay)
		i += 1
	GPIO.output(pin, GPIO.LOW)

#if x^2 + y^2 + z^2 > threshold
#somebody knock the door
def knock(threshold):
	global buffer
	if sys.version > '3':
		buffer = memoryview
	BUS = 1
	ADXL345_I2C_ADDR = 0x53
	pi = pigpio.pi() # open local Pi
	h = pi.i2c_open(BUS, ADXL345_I2C_ADDR)
	if h >= 0: # Connected OK?
		# Initialise ADXL345.
		pi.i2c_write_byte_data(h, 0x2d, 0)  # POWER_CTL reset.
		pi.i2c_write_byte_data(h, 0x2d, 8)  # POWER_CTL measure.
		pi.i2c_write_byte_data(h, 0x31, 0)  # DATA_FORMAT reset.
		pi.i2c_write_byte_data(h, 0x31, 11) # DATA_FORMAT full res +/- 16g.
		read = 0
	#get initial pos
	(s, b) = pi.i2c_read_i2c_block_data(h, 0x32, 6)
	if s >= 0:
		(init_x,init_y,init_z) = struct.unpack('<3h', buffer(b))
	#loop until someone move the sensor
	while 1:
		(s, b) = pi.i2c_read_i2c_block_data(h, 0x32, 6)
		if s >= 0:
			(x,y,z) = struct.unpack('<3h', buffer(b))
		if (init_x - x)**2 + (init_y - y) ** 2 + (init_z - z) ** 2 >= threshold:
			break
		time.sleep(0.01)
Trig_Pin =20
Echo_Pin =21

GPIO.setmode(GPIO.BCM)
GPIO.setup(Trig_Pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)
print ('test')
time.sleep(2)

def checkdist():
    GPIO.output(Trig_Pin, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(Trig_Pin, GPIO.LOW)
    while not GPIO.input(Echo_Pin):
        pass
    t1 = time.time()
    while GPIO.input(Echo_Pin):
        pass
    t2 = time.time()
    return (t2-t1)*340*100/2
'''
try:
    while True:
        print ('Distance:%0.2f cm'%checkdist())
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
'''
# Start from here.......
knock(1000)

print("Welcome to our security door!")
os.system('aplay welcome.wav')
print("You have two choose:")
print("		1. Open the door")
print("		2. Talk with the door")
os.system('arecord --device=plughw:1,0 --format S16_LE --rate 16000 -d 5 -c1 oneOrTwo.wav&')#record one or two
#Countdown
light(11, 5, 1)
audioFile = "oneOrTwo.wav"

visual_recognition = VisualRecognitionV3(
    '2018-05-18',
    api_key='809f50b16870162a1377fb579c2f610321ea2420')

with open('img/bill.jpg', 'rb') as images_file:
    faces = visual_recognition.detect_faces(images_file)
#print(json.dumps(faces, indent=2))


import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2018-05-18',
    api_key='809f50b16870162a1377fb579c2f610321ea2420')

with open('img/bill.jpg', 'rb') as images_file:
    faces = visual_recognition.detect_faces(images_file)
#print(json.dumps(faces, indent=2))

import Image


image = Image.open('img/bill.jpg')

genders=[]
ages=[]
face_location=[]
singles_info=[]
for imas in faces["images"]:
	for ima in imas["faces"]:
		fl = ima["face_location"]
		fg = ima["gender"]
		fa = ima["age"]
		genders.append(fg)
		ages.append(fa)
		face_location.append(fl)
	singles_info.append([face_location,genders,ages])
print(singles_info[0][0][0]["left"]) #第一张图的第一张脸的位置信息
