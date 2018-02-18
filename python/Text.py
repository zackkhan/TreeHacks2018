import cv2
import requests
import speech_recognition as sr
from os import path
from pprint import pprint

class Text: 
    def __init__(self):
        self.subscription_key = "e552bd5890934ed595dbf8d7fd05816f"
        self.speech_to_text_key = "2ed41467970e4791bec9a48388bb416e"
        self.text_analytics_base_url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/"
        self.language_api_url = self.text_analytics_base_url + "languages"
        self.sentiment_api_url = self.text_analytics_base_url + "sentiment"
        self.key_phrase_api_url = self.text_analytics_base_url + "keyPhrases"  

    def extract_text_from_audio(self,audio_path):
        audio_file = path.join(path.dirname(path.realpath('__file__')), audio_path)
        r = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
        try:
            raw_text = r.recognize_bing(audio, key=self.speech_to_text_key)
            document = {'documents' : [
            {'id': '1', 'language': 'en', 'text': raw_text}
            ]}
            return(document)
        except sr.UnknownValueError:
            return("Microsoft Bing Voice Recognition could not understand audio")
        except sr.RequestError as e:
            return("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))

def get_sentiment(self,document):
    headers   = {"Ocp-Apim-Subscription-Key": self.subscription_key}
    response  = requests.post(self.sentiment_api_url, headers=headers, json=document)
    sentiments = response.json()
    return(sentiments['documents'][0]['score'])

def get_keywords(self,document):
    headers   = {"Ocp-Apim-Subscription-Key": self.subscription_key}
    response  = requests.post(self.key_phrase_api_url, headers=headers, json=document)
    key_phrases = response.json()
    return(key_phrases['documents'][0]['keyPhrases'])