#! python3
import datetime as dt
import praw as pw
import praw,requests,re
import os
#format the comment to fit a line and be ready for poem processing
#leave only dots
def formatProcess(comment):
    outputString = comment.replace('\n','')
    outputString = outputString.replace('?','.').replace('!','.')
    outputString = re.sub(r'\.{2,}','.',outputString)
    outputString =re.sub(r'([^\s\w.]|_)+', '', outputString)
    return outputString[0:min(254,len(comment))].lower() + '\n'

#format the size of the comment only
def formatDisplay(comment):
    outputString = comment.replace('\n','')
    outputString =re.sub(r'([^\s\w.!*,:;@/\+--=#[]{}<>$£\']|_)+', '', outputString)
    return outputString[0:min(254,len(comment))] +'\n'

reddit = pw.Reddit(client_id='C-u-vJYPUPLdfg',
                     client_secret='Hyw3NkOJrL6qufVnIgt7EZ7Xj8k',
                     password='password123',
                     user_agent='roastr',
                     username='roastr123')
subreddit = reddit.subreddit('RoastMe')


max_submissions = int(input('amount of submissions to fetch: '))
max_comments = int(input('comments per submission: '))

top_submissions = subreddit.top(limit=max_submissions)


print(reddit.user.me());

#create directories
path = os.getcwd() + "/trainingSet"
pathImg = path + "/faces"
pathTxt = path + "/text"
os.mkdir(path);
print("the current working dir is %s" % path)
print("creating directories")

os.mkdir(pathImg)
os.mkdir(pathTxt)
os.mkdir(path + "/formatedRoasts")

#populate files
for i,submission in enumerate(top_submissions):
    print("processing submission: ",i+1)
    url = submission.url
    file_name = url.split("/")
    skip = False
    if len(file_name) == 0:
        file_name = re.findall("/(.*?)",url)
    file_name = file_name[-1]
    if "." not in file_name:
        skip = True
    if skip:
        continue
    parts = file_name.split('.')
    file_name = '.'+parts[-1]
    print(file_name)
    r = requests.get(url)
    with open(pathImg+"/roast"+str(i)+file_name,"wb+") as f:
        f.write(r.content)

    submission.comment_sort = 'top'
    submission.comments.replace_more(limit=max_comments)
    comments = submission.comments
    with open(pathTxt+"/roast"+str(i)+".txt","w+") as f:
        for j,top_level_comment in enumerate(comments):

            f.write(formatDisplay(top_level_comment.body))
            f.write(formatProcess(top_level_comment.body))
            with open (path+"/formatedRoasts/roastDatabase.txt","a") as g:
                g.write(formatProcess(top_level_comment.body))

            if j == max_comments-1:
                break
    if i == max_submissions-1:
        break
