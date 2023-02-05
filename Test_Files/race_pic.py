# This is for opening web cam and detecting your face and emotion

import cv2
from deepface import DeepFace

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)

while True:

    img = cv2.imread('hana_crop_test.jpg')  # loaď image
    color_img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = DeepFace.analyze(color_img_RGB, actions=['race'], enforce_detection=False)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, 1.1, 4)  # dectecting face

    # for drawing rectangle on detected face
    for (x, y, u, v) in faces:
        cv2.rectangle(img, (x, y), (x + u, y + v), (0, 255, 0), 2)

    # for putting text on img
    print(result[0])

    cv2.putText(img, result[0]['dominant_race'], (50, 50), font, 3, (0, 0, 255), 2, cv2.LINE_4)

    cv2.imshow('original video', img)

    # for closing cam press 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    x = input()

cap.release()
cv2.destroyAllWindows()