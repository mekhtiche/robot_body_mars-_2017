#!/usr/bin/python
import os
import json


path = "/home/odroid/catkin_ws/src/robot_body/recording/data_base/"
dir = os.listdir(path)
for file in dir:
    if file[-5:]==".json":
        with open(file, 'rw') as sign:
            movement = json.load(sign)
            movement["emotion_name"]=''
            movement["text"] = []
            movement["emotion_time"] = ''
print "done"
