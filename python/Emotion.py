import cv2
import dlib
import imutils
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from imutils import face_utils
from matplotlib import patches
from io import BytesIO
import requests

class Emotion: 
    def __init__(self):
        self.subscription_key = "34162b79f80a44f58c6629a083929c15"
        self.face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'
        self.headers = { 'Ocp-Apim-Subscription-Key': self.subscription_key }
        self.params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
        }
        self.all_emotions = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']

    def annotate_image(self, image_url):
        response = requests.post(self.face_api_url, params=self.params, headers=self.headers, json={"url": image_url})
        faces = response.json()

        #image_file = BytesIO(requests.get(image_url).content)
        image = Image.open(image_url)
        #image = Image.open(image_file)
        for face in faces:
            print(face)
            fr = face["faceRectangle"]
            fa = face["faceAttributes"]
            emotions = fa["emotion"]
            emotion = max(emotions, key=lambda key: emotions[key])
            return emotion