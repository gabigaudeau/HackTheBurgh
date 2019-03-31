import requests
import time
import praw as pr
import json
import face_recognition
import numpy as np
import re,sys,os
import operator
import random
import socket
import datetime


url = 'https://www.reddit.com/r/RoastMe/'
r = pr.Reddit(client_id='C-u-vJYPUPLdfg',
                     client_secret='Hyw3NkOJrL6qufVnIgt7EZ7Xj8k',
                     redirect_uri='http://localhost:8080',
                     user_agent='roastr scraper')

#to get r's trust we need an access token from their api
handle = 'https://api.pushshift.io/reddit/search/submission/?'
handleC = 'https://api.pushshift.io/reddit/search/comment/?'
handleComment = 'https://api.pushshift.io/reddit/submission/comment_ids/'
#POST data included in the URL, kinda like an attachment
#we're asking for Client_credentials Flow for non-installed script type app

#username = 'l_IBFD5bZOT_IA'
#password = 'CYdIMyeTNQrzIQb1qXBdwM71rms'
#encoded = base64.b64encode(username+':'+password)
#!/usr/bin/env python

#r = pr.Reddit(client_id='C-u-vJYPUPLdfg',
#                 client_secret='Hyw3NkOJrL6qufVnIgt7EZ7Xj8k',
#                 redirect_uri='http://localhost:8080',
#                 user_agent='roastr scraper')

def receive_connection():
    """Wait for and then return a connected socket..

    Opens a TCP connection on port 8080, and waits for a single client.

    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send('HTTP/1.1 200 OK\r\n\r\n{}'.format(message).encode('utf-8'))
    client.close()


def refresh_token():
    """Provide the program's entry point when directly executed."""
    if len(sys.argv) < 2:
        print('Usage: {} SCOPE...'.format(sys.argv[0]))
        return 1

    state = str(random.randint(0, 65000))
    url = r.auth.url(sys.argv[1:], state, 'permanent')
    print(url)

    client = receive_connection()
    data = client.recv(1024).decode('utf-8')
    param_tokens = data.split(' ', 2)[1].split('?', 1)[1].split('&')
    params = {key: value for (key, value) in [token.split('=')
                                              for token in param_tokens]}

    if state != params['state']:
        send_message(client, 'State mismatch. Expected: {} Received: {}'
                     .format(state, params['state']))
        return 1
    elif 'error' in params:
        send_message(client, params['error'])
        return 1

    refresh_token = r.auth.authorize(params['code'])
    send_message(client, 'Refresh token: {}'.format(refresh_token))
    return 0

# Print iterations progress
def progress(count, total, status=''):

    bar_len = 30
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def requestAndWrite(url,filename):
    with open(filename+'.json','w') as f:
        r = requests.get(url).json()
        json.dump(r,f)

def jsonToDict(filename):
    with open (filename,'r') as f:
        datastore = json.load(f)
    return datastore

def requestToDict(url):
    try:
        r = requests.get(url).json()
    except:
        print("cannot receive json from reddit, retrying...")
        time.sleep(5)
        return requestToDict(url)
    return r

lolz = ["somebody once told me the world is gonna roll me","dads are like boomerangs.. I hope","to live is to suffer","to survive is to find meaning in the suffering","stay cool","I <3 you to byts","I always start counting from 0","you're my wonderwall","did you know finland is a myth?","how you doin lars?","OwO what's this senpai","UwU","hey there fiona","wassu wassu wassuuuup","java needs to die","roses are red, violets are blue, your code don't work, and your face is like poop","abracadabra","loading poorly timed puns [========--] ...90%","yoooooooooooo","Kelechi is an absolute unit","how do you do fellow hooman","what's updog","mommy !?","daddy !?","Owo what's this","i heard you like bits","what's the point anymore","Norway doesn't exist either","the janek sends his regards","The Secret Life of Walter Mitty is a good movie 10/10","you owe me a beer",""]
#given json list of comments from subr get top n comments by score
#have to have fields=[id]

def loadSubmissions(table,comments_threshold,startDay=1,subreddit='roastme'):
    const_args = '&limit=500&fields=url,title,num_comments,score,created_utc,id&sort_type=num_comments&sort=desc'
    baseurl = handle + '&subreddit='+ subreddit + const_args

    submissions = table
    before = str(startDay) + 'd'
    after = str(startDay+1) + 'd'

    data_dict = requestToDict(baseurl+'&after='+after+'&before='+before)

    data = data_dict["data"]

    if len(data) == 0:
        print("NO MORE DATA, could not get requested number, found: "+str(submissions_count))
        return []

#UNTESTED\
    for index,dict in enumerate(data):
        if dict["num_comments"] < comments_threshold:
            data.pop(index)
#UNTESTED/
    submissions.extend(data)
        #print("current count: " + str(submissions_count))
    return startDay
#given a list of submission dictionaries update their score fields and remove ones
#without comments or below upvote threshold
def updateSubmissions(submissions,limit,score_threshold,comments_threshold):

    new = []
    try:
        for index,sub_dict in enumerate(submissions):
            id = sub_dict["id"]
            pr_submission = pr.models.Submission(r,id)
            ratio_complete = len(new)/limit
            ratio_through = index/(len(submissions)-1)
            used_ratio = ratio_complete if ratio_complete > ratio_through else ratio_through
            progress_suffix = '(c)' if ratio_complete > ratio_through else '(t)'
            progress(used_ratio,1,progress_suffix + 'encoding batch of:' + str(len(submissions)))
            if(len(new) >= limit):
                return new

            if not (pr_submission.num_comments <= comments_threshold or pr_submission.score <= score_threshold \
            or not (pr_submission.url.endswith(('.png','.jpg')))):
                copied_submission = submissions[index].copy()
                file_name = pr_submission.url.split('/')[-1].split('.')[-1]

                with open('temp.'+file_name,'wb') as f:
                    try:
                        picture = requests.get(pr_submission.url)
                    except:
                        print("couldn't load a picture, skipping ^-^")
                        continue

                    f.write(picture.content)
                    encodings = encodePicture('temp.'+file_name,False)# MAKE SURE FALSE
                    if len(encodings) != 0:
                        copied_submission["score"] = pr_submission.score
                        copied_submission["comments"] = loadTopComments(id,comments_threshold)
                        copied_submission["encodings"] = encodings
                        new.append(copied_submission.copy())
    except:
        print("some request failed in the batch, retrying the batch...")
        refresh_token()
        time.sleep(10)
        return updateSubmissions(submissions,limit,score_threshold,comments_threshold)
    return new

def loadTopComments(id,limit):

    try:
        pr_submission = pr.models.Submission(r,id)
        pr_submission.comment_sort = 'best'
        submission_comments = pr_submission.comments
        submission_comments.replace_more(limit=0)
    except:
        print("something oopsied in comments, refreshing and retrying ^_^")
        time.sleep(10)
        refresh_token
        return loadTopComments(id,limit)
    comments = []
    for index,top_level_comment in enumerate(submission_comments):
        comments.append(formatComment(top_level_comment.body))
        if (index+1) >= limit:
            break
    return comments

def encodePicture(filename,test):
    if test:
        return "[ ]"
    #for a dry run through to check for html errors
    try:
        pic = face_recognition.api.load_image_file(filename)
    except:
        return []
    encodings = face_recognition.api.face_encodings(pic)
    faces = []
    for encoding in encodings:
        faces.append(np.array2string(encoding))
    return faces

#given a list of dictionaries of submissions merge comments and format for poem
def getAllComments(data):
    formated_comments = []
    for index,dict in enumerate(data):
        comments = dict["comments"]
        for comment in comments:
            formated_comments.append(formatComment(comment)) #NOW JUST APPENDING PLAIN COMMENTS YOU CAN USE formatToPoem to get clean commets
    return formated_comments

#----------------------------USEFUL PUBLIC STUFF ------------------------------#

#give it the datafile name of the database and will create linguistic database with filename

def writeAllFormatedComments(datafile,filename,overwrite = False):
    if overwrite:
        overwriteData(getAllComments(loadData(datafile)),filename)
    else:
        saveData(getAllComments(loadData(datafile)),filename)

def writeCommentsToFile(dicts,filename,overwrite = False):
    if overwrite:
        overwriteData(getAllComments(dicts),filename)
    else:
        saveData(getAllComments(dicts),filename)

#this is just for general clean up
def formatComment(comment):
    return bytes(comment.strip(),'utf-8').decode('utf-8','ignore')




#fiona use this to format, if isn't as clean as you need, make changes here
def formatToPoem(comment):
    newlines = re.sub(r'\n',' ',comment.lower().strip('. '))
    punctuated = re.sub(r'[!?]','.',newlines)
    repetitions = re.sub(r'(([^A-Za-z])\2\2*)',r'\2',punctuated)
    characterReptitions = re.sub(r'((.)\2\2\2*)',r'\2',repetitions)
    result = re.sub('[^A-Za-z.\"\' ]','',characterReptitions)
    return result


#filepath without extension !
#will append existing data if same file exists
def saveData(data,filename):
    if not os.path.isfile(filename+'.json'):
        with open(filename+'.json','w') as f:
            json.dump(data,f)
    else:
        feeds = loadData(filename)

        feeds.extend(data)
        with open(filename+'.json',mode = 'w') as f:
            f.write(json.dumps(feeds))

def overwriteData(data,filename):
        with open(filename+'.json',mode = 'w+') as f:
            f.write(json.dumps(data))

#will pull into list of dictionaries
def loadData(filename):
    with open(filename+'.json','r') as f:
        return json.load(f)

def prettyPrintSortedByDate(list_of_dicts):
    #list_of_dicts.sort(key=operator.itemgetter('created_utc'))
    max_len = 50
    strings = []
    for dict in sorted(list_of_dicts, key = lambda dict : dict["created_utc"]):
        title = dict['title']
        diff = max(max_len - len(title),0)
        time_ago = datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(round(int(dict['created_utc'])))
        string = title[:50] +(' '*diff) +',' + "{:.2f}".format(time_ago.total_seconds()/86400) + ',' + str(dict['score'])
        strings.append(title + ':' + str(time_ago))
        print(string)
    return strings
#the sub has around 236,000 submissions over 3 years
#takes in:
#filename for data, ling data
#amount of submissions to pull
#minimum upvotes (too high might end up with not many submissions)
#minimum comments (same as comments pulled)
#optional - days offset (integer how many days ago to start indexing)
#all you need, right here, filenames are paths without extension
def createDatabase(data_filename,linguistic_filename,limit=10,upvote_threshold=50,comment_threshold=3,days_offset=1):
    curr_startDay = days_offset
    submissions_count = 0
    if refresh_token():
        #if managed to get refresh token
        print("*hacker voice* we're in")
    else:
        print("couldn't connect to r")

    while submissions_count < limit:
        print('\n')
        progress(submissions_count,limit,'processing')
        print('\n')
        submissions_batch = []
        capacity = limit - submissions_count

        loadSubmissions(submissions_batch,comment_threshold,curr_startDay)
        #if we cross over 1000 requests with this batch refresh token
        if ((submissions_count % 1000) + len(submissions_batch) >= 499):
            refresh_token() #get refresh token now and then

        submissions_batch = updateSubmissions(submissions_batch,min(capacity,len(submissions_batch)),upvote_threshold,comment_threshold)

        curr_startDay +=1

        batch_count = len(submissions_batch)

        saveData(submissions_batch[:capacity],data_filename)
        submissions_count += batch_count
        writeCommentsToFile(submissions_batch,linguistic_filename)

        print("\n           -----Progress------         ")
        print("batch of " + str(batch_count) + ' saved, now on posts from ' + str(curr_startDay) + ' days ago')
        print("total so far: " + str(submissions_count))
        print("\""+lolz[random.randint(0,len(lolz)-1)]+"\"")
        print("\n           -----Progress------         ")

    print("finished with " + str(submissions_count) + " submissions and on day " + str(curr_startDay) + " from now")

def findDuplicatesA(dicts):

    sorted_list = sorted(dicts,key = lambda x : x["id"])

    for i in range(len(sorted_list)-1,0,-1):
        if sorted_list[i]["id"] == sorted_list[i-1]["id"]:
            print("dup at: " + str(i) + ',' + str(i-1) + str(sorted_list[i]["id"]))
            del sorted_list[i]
    return sorted_list

def findDuplicatesB(comments):
    sorted_list = sorted(comments)

    for i in range(len(sorted_list)-1,0,-1):
        if sorted_list[i] == sorted_list[i-1]:
            print("dup at: " + str(i) + ',' + str(i-1) + str(sorted_list[i]))
            del sorted_list[i]
    return sorted_list

def validateDatabase(filename,filenameL):

    data = loadData(filename)

    new = findDuplicatesA(data)
    overwriteData(new,filename)
    writeAllFormatedComments(filename,filenameL,True)

def main():
    data_filename = input("path + filename (no extension) for datafile: ")
    ling_filename = input("path + filename (no extension) for commentFile: ")
    limit = int(input("amount of submissions to fetch (290000 for all): "))
    min_karma = int(input("how many upvotes needed for post to be included (10 recomended): "))
    min_comments = int(input("how many comments to pull per post (will skip ones with not enough comments): "))
    offset = int(input("fetching offset in days counting backwards from today (1 - infinity): "))
    createDatabase(data_filename,ling_filename,limit,min_karma,min_comments,offset)
    validateDatabase(data_filename,ling_filename)

if __name__ == "__main__":
    main()
