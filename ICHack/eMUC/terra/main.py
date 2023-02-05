import requests
import time
import numpy as np
from deepface import DeepFace
import cv2
# from threading import Thread

import matplotlib.pyplot as plt

jsurl = 'http://146.169.183.21:8888'


def get_data():

    res = requests.get(jsurl + "/api/hr")
    hr = res.text
    hr = hr[1:-1]
    hr = hr.split(",")
    hr = [int(i) for i in hr]
    return hr


def get_samples(n):
    requests.get(jsurl + "/reset")
    time.sleep(n)

    return get_data()


def emotionAnalysis(frame):
    # function to analyse images. Returns dictionary with age, gender, race and emotion
    faces = DeepFace.extract_faces(frame, target_size=(300, 300), align=True, detector_backend='mtcnn')
    # print(len(faces))
    # for face in faces:
    #     print(face)
    facialCoords = faces[0]['facial_area']
    img = frame
    blank = np.zeros(img.shape[:2], dtype='uint8')
    startPoint = (round(facialCoords['x'] * 0.85), round(facialCoords['y'] * 0.85))
    endPoint = (
        round((facialCoords['x'] + facialCoords['w']) * 1.15), round((facialCoords['y'] + facialCoords['h']) * 1.15))
    mask = cv2.rectangle(blank, startPoint, endPoint, 255, -1)
    masked = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow('Output', masked)
    cv2.imwrite('test.jpg', masked)

    objs = DeepFace.analyze(masked, actions=['emotion'])[0]
    print(objs['emotion'])
    return (objs['dominant_emotion'], objs["emotion"][objs['dominant_emotion']])


# BASELINE = np.mean(get_samples(30))
def get_emotion():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        a = 0
    while True:
        time.sleep(2)
        ret, frame = cap.read()

        try:
            return emotionAnalysis(frame)

        except:
            a = 0

        time.sleep(2)


def excitement(heart_rate_data):
    rr_intervals = []
    for i in range(1, len(heart_rate_data)):
        rr_intervals.append(heart_rate_data[i] - heart_rate_data[i - 1])
    #
    avg_rr_interval = np.mean(rr_intervals)
    std_rr_interval = np.std(rr_intervals)
    if avg_rr_interval == 0:
        return 0
    excitement_level = (avg_rr_interval - std_rr_interval) / avg_rr_interval
    return int(excitement_level)


def moving_average(arr):
    moving_avg = []
    for i in range(len(arr) - 2 + 1):
        moving_avg.append(sum(arr[i:i + 2]) / 2)
    return moving_avg


def score():
    exval = excitement(moving_average(get_samples(6)))
    emotion, confidence = get_emotion()

    if (emotion == "angry"):  # happy
        escore = 0.2

    elif (emotion == "disgust"):
        escore = 0.4

    elif (emotion == "fear"):
        escore = 0.5

    elif (emotion == "sad"):
        escore = 0.6

    elif (emotion == "neutral"):
        escore = 1

    elif (emotion == "happy"):
        escore = 1.5

    elif (emotion == "surprise"):
        escore = 2

    return (escore * confidence * exval * 0.01)

eth = ["Arab", "Pakisani", "Middle Eastern", "White", "Arab F", "Black M", "Black F", "Asian", "Greek", "Macedonian"]
res=[]
for i in range(10):
    res.append(score())
maxi= max(res)
ind= res.index(maxi)
print(f'max score @ image no {ind}' + eth[ind])

