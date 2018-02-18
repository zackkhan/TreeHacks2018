import cv2
import requests
import subprocess
import Speech
from Speech import *
import time
import json
import os

def get_frames(): 
    vidcap = cv2.VideoCapture('long_test.webm')
    success,image = vidcap.read()
    count = 0
    success = True
    speech = Speech()
    analysis_list = []
    start = time.time()
    #avg = {}
 
    while success:
        success, image = vidcap.read()
        if (count % 50 == 0):
            cv2.imwrite("frame%d.jpg" % count, image)     
            analysis = {}
            analysis['time'] = time.time() - start
            img = "frame%d.jpg" % count
            analysis['expression'], head_info = speech.emotions_from_image(img)
            #analysis['roll'] = head_info['roll']
            #analysis['pitch'] = head_info['pitch']
            #analysis['yaw'] = head_info['yaw']
            #print(head_info)
            analysis_list.append(analysis)
        count += 1
    command = "ffmpeg -i long_test.webm -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    hasSound = False
    for fname in os.listdir('.'):
        if fname.endswith('.wav'):
            hasSound = True
    if not(hasSound):
        subprocess.call(command, shell=True)
    document = speech.speech_to_text('audio.wav')
    idx = 0
    count = 0
    k = 1
    doc = document['documents'][0]['text']
    split_document = speech.split_string(doc, k)
   
    section = int(len(analysis_list) / len(split_document))
    while idx < len(analysis_list) and count < len(split_document):
        txt = split_document[count]
        temp_document = {'documents': [{'id': '1', 'language': 'en', 'text': txt}]}
        sentiment = speech.extract_sentiment(temp_document)
        #avg['sentiment'] += sentiment
        keywords = speech.extract_keywords(temp_document)
        search_results = []
        for w in keywords: 
            y = speech.get_search_results(w)
            search_results.append(y)
        for i in range(section):
            if idx + i < len(analysis_list):
                analysis_list[idx + i]['text'] = txt
                analysis_list[idx + i]['sentiment'] = sentiment
                analysis_list[idx + i]['keywords'] = keywords
                analysis_list[idx + i]['search_results'] = search_results     
        idx += section
        count += 1
    #avg['sentiment'] /= len(analysis_list)
    print(json.dumps(analysis_list))
get_frames()
