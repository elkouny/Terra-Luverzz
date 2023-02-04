# code to go through all photos in a images folder next to this file
# categorises all images and outputs a list of dictionaries assertaining to each image
# assumes files are jpg
import glob
import os.path

# get current path
currentPath = os.getcwd()
print(currentPath)

# image file path
imagesPath = currentPath + '\\images'
imagesFolderExist = os.path.exists(imagesPath)
while not imagesFolderExist:
    print("Error, no images directory")
    imagesFolderExist = os.path.exists(imagesPath)

imageTypePath = currentPath + '\\images\\*.jpg'
print(imageTypePath)
fileLocations = glob.glob(imageTypePath)
fileNames = []
for file in fileLocations:
    fileNames.append(file.split("\\")[-1])
print(fileNames)



