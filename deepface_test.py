from deepface import DeepFace
import cv2

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
faceNet = cv2.dnn.readNet(faceModel, faceProto)
padding = 20


def getFaceBox(net, frame, conf_threshold=0.75):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)

    return frameOpencvDnn, bboxes

frame = cv2.imread('hana_sat_test.jpg')
# creating a smaller frame for better optimization
small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
frameFace, bboxes = getFaceBox(faceNet, small_frame)


for bbox in bboxes:

        face = small_frame[max(0, bbox[1] - padding):min(bbox[3] + padding, frame.shape[0] - 1),
               max(0, bbox[0] - padding):min(bbox[2] + padding, frame.shape[1] - 1)]
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        objs = DeepFace.analyze(img_path='hana_sat_test.jpg', actions=['age', 'gender', 'race', 'emotion'])

        print(objs)
        print(objs[0]['age'])
        print(objs[0]['dominant_gender'])
        print(objs[0]['dominant_race'])
        print(objs[0]['dominant_emotion'])
