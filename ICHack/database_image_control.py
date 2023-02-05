# code to go through all photos in a images folder next to this file
# categorises all images and outputs a list of dictionaries assertaining to each image
# assumes files are jpg
import glob
import os.path
from deepface import DeepFace
import cv2
import numpy as np
import sqlite3

# get current path
currentPath = os.getcwd()
print(currentPath)
dbPath = currentPath + '/db.sqlite3'
connection = sqlite3.connect(dbPath)
cursor = connection.cursor()


def imageAnalysis(imagePath):
    # function to analyse images. Returns dictionary with age, gender, race and emotion
    faces = DeepFace.extract_faces(img_path=imagePath, target_size=(300, 300), align=True, detector_backend='mtcnn')
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
    #print(objs)
    response = {'age': objs['age'],
                'gender': objs['dominant_gender'],
                'race': objs['dominant_race'],
                'emotion': objs['dominant_emotion']}


    return response


def dataListCreate(currentPath):
    imageTypePath = currentPath + '/*.jpg'
    print("Image type path:", imageTypePath)
    fileLocations = glob.glob(imageTypePath)
    print(fileLocations)
    fileNames = []
    for file in fileLocations:
        fileNames.append(file.split("/")[-1])

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


def getCurrentMaxId():
    # current max id for a photo, so we increment on that
    #sql = 'SELECT name FROM sqlite_schema WHERE type=\'table\' ORDER BY name;'
    sql = 'SELECT MAX(id) FROM eMUC_picture'
    maxId = cursor.execute(sql)
    maxId = maxId.fetchall()[0][0]
    if maxId == None:
        maxId = 0
    print(maxId)
    return maxId

def addImagesToDB(imagesPath, imageAttributeList, startMaxID):
    # loops through each image in imageAttributionList, adds each to database
    # sql for adding picture into database
    sql = 'INSERT INTO eMUC_picture(id, photo_path, age, sex, ethnicity) VALUES(?, ?, ?, ?, ?)'
    data = []
    for image in imageAttributeList:
        # start by incrementing id
        startMaxID += 1
        # get variables to add into database
        imagePath = str(imagesPath + '/' + image['fileName'])
        print(imagePath)
        age = image['age']
        gender = image['gender']
        ethnicity = image['race']
        
        tempData = (startMaxID, imagePath, age, gender, ethnicity)
        data.append(tempData)

    cursor.executemany(sql, data)
    connection.commit()


def addAll():
    # image file path testing
    imagesPath = currentPath + '/images'
    print(imagesPath)
    imagesFolderExist = os.path.exists(imagesPath)
    while not imagesFolderExist:
        print("Error, no images directory")
        raise SystemExit(0)

    print("Creating Data List")
    #dataList = dataListCreate(imagesPath)
    dataList = [{'fileName': 'Chris-Hemsworth.jpg',
                'age': 24,
                'gender': 'Man',
                'race': 'white'}]
    print("Data List: ", dataList)
    maleList, femaleList = maleFemaleSplit(dataList)
    print("Males")
    for list in maleList:
        print(list)

    print("\nFemales")
    for list in femaleList:
        print(list)


    
    maxId = getCurrentMaxId()
    addImagesToDB(imagesPath, dataList, maxId)


def deleteAll():
    sql = 'DELETE FROM eMUC_picture'
    cursor.execute(sql)
    connection.commit()


def removeOne(id):
    # removes one with specific id
    sql = 'DELETE FROM eMUC_picture WHERE id=='+str(id)+''
    cursor.execute(sql)
    connection.commit()



# control main
# allows option to delete all records, delete specific record and add all from images
while True:
    control = str(input("Enter command. DEL to delete all rows, REM to delete specific row, ADD to add all from images, Q to quit")).upper()
    if control == 'Q':
        break
    elif control == 'DEL':
        deleteAll()
    elif control == 'REM':
        removeOne(int(input("Enter id of row to delete")))
    elif control == 'ADD':
        addAll()
    else:
        print("Not valid input")






