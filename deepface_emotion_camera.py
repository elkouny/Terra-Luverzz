import time

from deepface import DeepFace
import cv2
import numpy as np


def emotionAnalysis(frame):
    # function to analyse images. Returns dictionary with age, gender, race and emotion
    faces = DeepFace.extract_faces(frame, target_size=(300, 300), align=True, detector_backend='mtcnn')
    print(len(faces))
    for face in faces:
        print(face)
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

    objs = DeepFace.analyze(masked,
                            actions=['age', 'gender', 'race', 'emotion'
                                     ])[0]

    return objs['dominant_emotion']


# setup camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    cap = cv2.VideoCapture(1)
if not cap.isOpened():
    raise IOError("cannot open")

while True:
    ret, frame = cap.read()
    try:
        emotion = emotionAnalysis(frame)
        print(emotion)
    except:
        print("No face")
    time.sleep(5)
    print("taking pic")
    time.sleep(2)
