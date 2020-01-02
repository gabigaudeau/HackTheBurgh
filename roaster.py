
import face_recognition
import numpy, re, sys, random
import json

#FROM SCRAPER FOR SIMPLICITY
#will pull into list of dictionaries
def loadData(filename):
    with open(filename+'.json','r') as f:
        return json.load(f)
#fiona use this to format, if isn't as clean as you need, make changes here
def formatToPoem(comment):
    newlines = re.sub(r'\n',' ',comment.lower().strip('. '))
    punctuated = re.sub(r'[!?]','.',newlines)
    repetitions = re.sub(r'(([^A-Za-z])\2\2*)',r'\2',punctuated)
    characterReptitions = re.sub(r'((.)\2\2\2*)',r'\2',repetitions)
    result = re.sub('[^A-Za-z.\"\' ]','',characterReptitions)
    return result


#FROM SCRAPER FOR SIMPLICITY


#THE FULL PATH + NAME + EXTENSION, returns array of encodings
def getEncodedingsInPic(filepath):
    try:
        pic = face_recognition.api.load_image_file(filepath)
        return face_recognition.api.face_encodings(pic)
    except Exception:
        return []
    

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
        rand = random.randint(0,len(dict["comments"])-1)
        roast_dict["comment"] = dict["comments"][rand]
        roast_dict["url"] = dict["url"]
        roast_dict["id"] = dict["id"]
        roast_dicts.append(roast_dict)
    return roast_dicts

#this is it, filename is pic name + path + EXTENSION
#datafile is just path + filename of database (NOT LINGO)
#will return all roasts for all faces in the picture

def roastMe(filename,datafile):
    roast_submissions = getSubmissionsByFaces(filename,datafile)
    roasts = selectRoasts(roast_submissions)
    return roasts


if __name__ == "__main__":
    print(roastMe('testVictim.jpg','database'))
