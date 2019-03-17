# import the libraries
import os
import face_recognition
import numpy as np

import random as rd

#def roast():
matches= os.listdir('unknown_face')
image_to_be_matched_encoded = None
for match in matches:
    image_to_be_matched = face_recognition.load_image_file('unknown_face/' + match)
image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]

    # iterate over each encodings
known_roasts=os.listdir('trainingset/text')
encodings=[]
distances = None
files=os.listdir('encodings')
for index, file in enumerate(files):
    readFile=open('encodings/'+file, "r")
    fileContents=readFile.read()
    encodings.append((np.fromstring(fileContents[1:-1].replace('\n',''), sep=' ')))
for j in range(0,len(encodings)):
    for i in range(len(encodings[0])):
        encodings[j][i] = rd.uniform(-1,1)
distances = face_recognition.face_distance(encodings, image_to_be_matched_encoded)

lowestDist= distances[0]
lowestIndex=0
for index, distance in enumerate(distances):
    if(distance<lowestDist):
        lowestDist=distance
        lowestIndex=index
    else:
        continue


rightRoastFile=open('trainingSet/text/' + known_roasts[lowestIndex])
print(rightRoastFile.readline())
#roast()
