import scraper as s
import datetime

#this script will automatically find out the last date of the last entry and extend the database
#by a thousand entries

dicts = s.loadData('database')
highest = 0

for dict in dicts:
    delta = datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(round(int(dict['created_utc'])))
    days_ago = delta.total_seconds() /86400
    highest = max(highest,days_ago)
print(highest)


s.createDatabase('database','lingobase',300000,10,10,round(highest + 1))
