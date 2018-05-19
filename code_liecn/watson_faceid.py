# encoding: utf-8
# !/usr/bin/env python
# This is a demo for face_detect
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