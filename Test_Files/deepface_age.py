import os
import time

from deepface import DeepFace
from retinaface import RetinaFace
from mtcnn import mtcnn
import matplotlib.pyplot as plt
import cv2
import numpy as np
imagePath = 'parisini_test.jpg'
faces = DeepFace.extract_faces(img_path=imagePath, target_size=(300,300) ,align=True, detector_backend='mtcnn')
print(len(faces))
for face in faces:
    print(face)
facialCoords = faces[0]['facial_area']
img = cv2.imread(imagePath)
blank = np.zeros(img.shape[:2], dtype='uint8')
startPoint = (round(facialCoords['x']*0.85), round(facialCoords['y']*0.85))
endPoint = (round((facialCoords['x'] + facialCoords['w'])*1.15), round((facialCoords['y'] + facialCoords['h'])*1.15))
mask = cv2.rectangle(blank, startPoint, endPoint, 255, -1)
masked = cv2.bitwise_and(img, img, mask=mask)
#cv2.imshow('Output', masked)
cv2.imwrite('test.jpg', masked)


objs = DeepFace.analyze(masked,
    actions = ['age', 'gender', 'race','emotion'
   ])

print(objs)

