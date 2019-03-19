import cv2
import os
import face_recognition
import numpy as np
from natsort import natsorted
# from scraper import formatProcess
# from roast_to_poem import main
import pyttsx3
import time


def faceFromCam(filepath):
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    engine = pyttsx3.init()
    # Create arrays of known face encodings and their names
    encodings = []
    files = natsorted(os.listdir('encodings'))
    for index, file in enumerate(files):
        readFile = open('encodings/'+file, "r", encoding="utf-8")
        if os.stat('encodings/'+file).st_size == 0:
            encodings.append(np.zeros((128,)))
            continue
        fileContents = readFile.read()

        encodings.append(np.fromstring(fileContents[1:-1].replace('\n', ''), sep=' '))
    known_roasts = natsorted(os.listdir('trainingset/text'))
    # Initialize some variables
    process_this_frame = True

    while True:
        lowestIndex = 0
        distances = []
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            if len(face_encodings) == 0:
                continue
            else:
                for face_encoding in face_encodings:
                    for encoding in encodings:
                        distances.append(face_recognition.face_distance(encoding, face_encodings))

                lowestDist = distances[0]
                for index, distance in enumerate(distances):
                    if distance < lowestDist:
                        lowestDist = distance
                        lowestIndex = index
                print(lowestIndex)
                try:
                    roast=known_roasts[lowestIndex]
                except IndexError:
                    continue
                with open('trainingSet/text/' + roast, encoding="utf-8") as f:
                    content = f.read()
                line = content.split('\n')[0]
                print(line)

                engine.say(line)
                engine.runAndWait()
                time.sleep(5)
        process_this_frame = not process_this_frame


'''         # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
'''
faceFromCam('templates')
