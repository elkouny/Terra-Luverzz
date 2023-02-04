# code to go through all photos in a images folder next to this file
# categorises all images and outputs a list of dictionaries assertaining to each image
# assumes files are jpg
import glob
import os.path
from deepface import DeepFace
import cv2
import numpy as np



def imageAnalysis(imagePath):
    # function to analyse images. Returns dictionary with age, gender, race and emotion
    faces = DeepFace.extract_faces(img_path=imagePath, target_size=(300, 300), align=True, detector_backend='mtcnn')
    print(len(faces))
    for face in faces:
        print(face)
    facialCoords = faces[0]['facial_area']
    img = cv2.imread(imagePath)
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
    print(objs)
    response = {'age': objs['age'],
                'gender': objs['dominant_gender'],
                'race': objs['dominant_race'],
                'emotion': objs['dominant_emotion']}


    return response


def dataListCreate(currentPath):
    imageTypePath = currentPath + '\\images\\*.jpg'

    fileLocations = glob.glob(imageTypePath)
    fileNames = []
    for file in fileLocations:
        fileNames.append(file.split("\\")[-1])

    imageData = []
    for fileIndex in range(0, len(fileNames)):
        # goes through each file, recieves the response from the image analysis,
        # adds the attributes to a dictionary with the file name
        # adds to list of files
        fileName = {'fileName': fileNames[fileIndex]}
        fullAttributes = dict(fileName, **imageAnalysis(fileLocations[fileIndex]))
        imageData.append(fullAttributes)

    return imageData


def maleFemaleSplit(dataList):
    maleList = []
    femaleList= []
    for imageAttribute in dataList:
        if imageAttribute['gender'] == 'Man':
            # male so add to male list
            maleList.append(imageAttribute)
        else:
            femaleList.append(imageAttribute)
    return maleList, femaleList



# get current path
currentPath = os.getcwd()
print(currentPath)

# image file path testing
imagesPath = currentPath + '\\images'
imagesFolderExist = os.path.exists(imagesPath)
while not imagesFolderExist:
    print("Error, no images directory")
    raise SystemExit(0)

dataList = dataListCreate(currentPath)
print(dataList)
maleList, femaleList = maleFemaleSplit(dataList)
print("Males")
for list in maleList:
    print(list)

print("\nFemales")
for list in femaleList:
    print(list)






