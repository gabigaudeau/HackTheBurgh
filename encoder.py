# make a list of all the available images
# import the libraries
import os
import face_recognition
import numpy as np

# Create directory
dirName = 'encodings'
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
except FileExistsError:
    print("Directory " , dirName ,  " already exists")


images= os.listdir('trainingSet/faces/')
for index,image in enumerate(images):
    current_image = face_recognition.load_image_file('trainingSet/faces/' + image)
    encoding = face_recognition.face_encodings(current_image)
    if (len(encoding)==0):
        continue
    else:
        actualImage = encoding[0]
        encodingFile=open("encodings/encoding"+str(index)+".txt","w+")
        encodingFile.write(np.array_str(actualImage))
        encodingFile.close()

known_roasts=[]
roasts=os.listdir('trainingSet/text/')
for roast in roasts:
    current_roast=open('trainingSet/text/' +roast, "r")
    roastline=(current_roast.readline())
    known_roasts.append(roastline)
