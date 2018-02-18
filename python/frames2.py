import cv2
import requests
import subprocess
import Text
from Text import *
import Emotion
from Emotion import *
import time
import json
import os

def get_frames(): 
    vidcap = cv2.VideoCapture('test.webm')
    success,image = vidcap.read()
    count = 0
    success = True
    analysis_list = []
    start = time.time()
    while success:
        success, image = vidcap.read()
        # print('Read a new frame: ', success)
        if (count % 100 == 0):
            cv2.imwrite("frame%d.jpg" % count, image)     
            emotion = Emotion()
            analysis = {}
            analysis['time'] = time.time() - start
            x = "frame%d.jpg" % count
            #analysis['expression'] = emotion.annotate_image(x)
            analysis_list.append(analysis)
        count += 1
    command = "ffmpeg -i test.webm -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    hasSound = False
    for fname in os.listdir('.'):
        if fname.endswith('.wav'):
            hasSound = True
    if not(hasSound):
        subprocess.call(command, shell=True)
    txt = Text()
    document = txt.extract_text_from_audio('audio.wav')
    print(json.dumps(analysis_list))
get_frames()
        


        
        














