# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import matplotlib.pyplot as plt
import numpy as np
import requests
import speech_recognition as sr
from io import BytesIO
from matplotlib import patches
from os import path
from PIL import Image
from pprint import pprint
from IPython.display import HTML


class Speech:
    def emotions_from_image(self, image_path):
        headers = {
            'Ocp-Apim-Subscription-Key': self.kEMOTION_KEY,
            'Content-type': 'application/octet-stream'
        }
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'headPose,emotion',
        }
        with open(image_path, 'rb') as f:
            img_data = f.read()
        response = requests.post(
            self.kEMOTION_URL, params=params, headers=headers, data=img_data)
        faces = response.json()
        fr = faces[0]["faceRectangle"]
        fa = faces[0]["faceAttributes"]
        headPose = fa["headPose"]
        emotions = fa["emotion"]
        emotion = max(emotions, key=lambda key: emotions[key])
        return emotion, headPose

    def speech_to_text(self, file_path):
        audio_file = path.join(path.dirname(
            path.realpath('__file__')), file_path)
        r = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = r.record(source)
        try:
            raw_text = r.recognize_bing(audio, key=self.kSPEECH_TO_TEXT_KEY)
            document = {'documents': [
                {'id': '1', 'language': 'en', 'text': raw_text}
            ]}
            return document
        except sr.UnknownValueError:
            return("Microsoft Bing Voice Recognition could not understand audio")
        except sr.RequestError as e:
            return("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

    def extract_sentiment(self, text):
        headers = {"Ocp-Apim-Subscription-Key": self.kTEXT_ANALYSIS_KEY}
        response = requests.post(
            self.kSENTIMENT_URL, headers=headers, json=text)
        sentiments = response.json()
        return sentiments['documents'][0]['score']

    def extract_keywords(self, text):
        headers = {"Ocp-Apim-Subscription-Key": self.kTEXT_ANALYSIS_KEY}
        response = requests.post(self.kKEY_PHRASE_URL,
                                 headers=headers, json=text)
        key_phrases = response.json()
        return key_phrases['documents'][0]['keyPhrases']

    def get_search_results(self, search_term):
        headers = {"Ocp-Apim-Subscription-Key": self.kSEARCH_KEY}
        params = {"q": search_term,
                  "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(
            self.kSEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        rows = "\n".join(["""<tr>
                           <td><a href=\"{0}\">{1}</a></td>
                           <td>{2}</td>
                         </tr>""".format(v["url"], v["name"], v["snippet"]) for v in search_results["webPages"]["value"]])
        return HTML("<table>{0}</table>".format(rows))

    def __init__(self):
        # Face API
        self.kEMOTION_KEY = "34162b79f80a44f58c6629a083929c15"
        self.kEMOTION_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'
        # Speech to Text API
        self.kSPEECH_TO_TEXT_KEY = "2ed41467970e4791bec9a48388bb416e"
        # Text Analysis API
        self.kTEXT_ANALYSIS_KEY = "e552bd5890934ed595dbf8d7fd05816f"
        text_analytics_base_url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/"
        self.kSENTIMENT_URL = text_analytics_base_url + "sentiment"
        self.kKEY_PHRASE_URL = text_analytics_base_url + "keyPhrases"
        # Bing Web API
        self.kSEARCH_KEY = "9db3ddee989743f48b738680d30c5bab"
        self.kSEARCH_URL = "https://api.cognitive.microsoft.com/bing/v7.0/search/"
