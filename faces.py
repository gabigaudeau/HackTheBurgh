# import the libraries
import os
import face_recognition
import numpy as np

def roast(filePath):
    matches= os.listdir(filepath)
    image_to_be_matched_encoded = none
    for match in matches:
    image_to_be_matched = face_recognition.load_image_file(filepath + match)

    image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]

    # iterate over each encodings
    distances = face_recognition.face_distance(known_encodings, image_to_be_matched_encoded)
    lowestDist=distances[0]
    lowestIndex=0
    for index, distance in enumerate (distances):
        if(distance<lowestDist):
            lowestDist=distance
            lowestIndex=index


    return(known_roasts[index])
