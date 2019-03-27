from scraper import loadData,formatToPoem
import face_recognition
import numpy, re, sys
#THE FULL PATH + NAME + EXTENSION, returns array of encodings
def getEncodedingsInPic(filepath):
    pic = face_recognition.api.load_image_file(filepath)
    return face_recognition.api.face_encodings(pic)

#for a single encoding, returns the id of submission
def findClosestEncoding(encoding,data):
    min = sys.maxsize
    minID = ""
    for dict in data:
        roast_encodings = parseEncodings(dict["encodings"])
        np_roast_encodings = numpy.asarray(roast_encodings)
        distances = face_recognition.api.face_distance(np_roast_encodings,encoding)
        (localMinI,localMin) = findSmallest(distances)
        if localMin < min:
            minID = dict["id"]
            min = localMin
    return minID

#get a numpy array from encodings passed as string
def parseEncodings(stringEncodings):
    encodings = []
    for stringEncoding in stringEncodings:
        stringEncoding = stringEncoding.strip('[]')
        stringEncoding = re.sub(r'\n','',stringEncoding)
        encodings.append(numpy.fromstring(stringEncoding,dtype = float, sep= ' '))
    return encodings

def findSmallest(list):
    min = sys.maxsize
    minI = 0
    for index,distance in enumerate(list):
        if distance <= min:
            min = distance
            minI = index
    return (minI,min)

#returns all submissions for the given disgraceful faces
#filepath is full path + filename + extension
#dataname is just filepath + filename of json database,
def getSubmissionsByFaces(filepath,dataname):

    victim_encodings = getEncodedingsInPic(filepath)
    #list of dicts
    roasting_data = loadData(dataname)

    roast_submission_ids = []
    for encoding in victim_encodings:
        roast_submission_id = findClosestEncoding(encoding,roasting_data)
        roast_submission_ids.append(roast_submission_id)

    submissions = []
    for id in roast_submission_ids:
        submissions.append([x for x in roasting_data if x["id"] == id][0])

    return submissions
#select roast from a list of submissions
def selectRoasts(submission_dicts):
    roast_dicts = []
    for dict in submission_dicts:
        roast_dict = {}
        #for now choose first top comment for each face
        roast_dict["comment"] = dict["comments"][0]
        roast_dict["url"] = dict["url"]
        roast_dicts["id"] = dict["id"]
        roast_dicts.append(roast_dict)
    return roast_dicts

#this is it, filename is pic name + path + EXTENSION
#datafile is just path + filename of database (NOT LINGO)
#will return all roasts for all faces in the picture

def roastMe(filename,datafile):
    roast_submissions = getSubmissionsByFaces(filename,datafile)
    roasts = selectRoasts(roast_submissions)
    return roasts

print(roastMe('testVictim.jpg','database'))
