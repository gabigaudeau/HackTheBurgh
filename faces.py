# import the libraries
import nltk
import os
import face_recognition
import numpy as np
from natsort import natsorted
from scraper import formatProcess
from roast_to_poem import main


# absolute bath
def roast(imgpath):

    image_to_be_matched = face_recognition.load_image_file(imgpath)
    image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)
    known_roasts = natsorted(os.listdir('trainingset/text'))
    encodings = []
    files = natsorted(os.listdir('encodings'))
    for index, file in enumerate(files):
        readFile=open('encodings/'+file, "r", encoding="utf-8")
        if os.stat('encodings/'+file).st_size == 0:
            encodings.append(np.zeros((128,)))
            continue
        fileContents = readFile.read()

        encodings.append(np.fromstring(fileContents[1:-1].replace('\n', ''), sep=' '))
    distances = []
    for encoding in encodings:
        distances.append(face_recognition.face_distance(encoding, image_to_be_matched_encoded))

    lowestDist = distances[0]
    lowestIndex = 0
    for index, distance in enumerate(distances):
        if(distance < lowestDist):
            lowestDist = distance
            lowestIndex = index
        else:
            continue
    path = os.getcwd() + "/"
    with open('trainingSet/text/' + known_roasts[lowestIndex], encoding="utf-8") as f:
        content = f.read()
    line = content.split('\n')[0]
    print(line)
    return line
    # main(formatProcess(line),"C:/Users/Lars Thalian/Documents/GitHub/HackTheBurgh/trainingSet/formatedRoasts/roastDatabase.txt","C:/Users/Lars Thalian/Documents/GitHub/HackTheBurgh/phodict.txt")
    # roast(os.getcwd()+ "/unknown_face/roast15.jpg" )
