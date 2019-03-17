# import the libraries
import os
import face_recognition
import numpy as np
from natsort import natsorted
from scraper import formatProcess
#absolute bath
def roast(imgpath):
    #matches = os.listdir('unknown_face')
    #image_to_be_matched = None
    #for match in matches:
#        image_to_be_matched = face_recognition.load_image_file('unknown_face/' + match)
#    image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]
    image_to_be_matched_encoded = face_recgonition.face_encoding(imgpath)
        # iterate over each encodings
    known_roasts=natsorted(os.listdir('trainingset/text'))
    encodings=[]
    distances = None
    files=natsorted(os.listdir('encodings'))
    for index, file in enumerate(files):
        readFile=open('encodings/'+file, "r", encoding="utf-8")
        if os.stat('encodings/'+file).st_size==0:
            encodings.append(np.zeros(128))
            continue
        fileContents=readFile.read()
        encodings.append((np.fromstring(fileContents[1:-1].replace('\n',''), sep=' ')))
    distances = face_recognition.face_distance(encodings, image_to_be_matched_encoded)

    lowestDist= distances[0]
    lowestIndex=0
    for index, distance in enumerate(distances):
        if(distance<lowestDist):
            lowestDist=distance
            lowestIndex=index
        else:
            continue

    rightRoastFile=open('trainingSet/text/' + known_roasts[lowestIndex], encoding="utf-8")
    return rightRoastFile.readLine()
    #roast()
