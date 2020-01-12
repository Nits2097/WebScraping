from bs4 import BeautifulSoup
import urllib.request
import csv
import datetime

'''
open the requested url
parse the html page
extract the given table values
store all rows of the table in results
'''
ans={}
urlLink =  'https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches'
link = urllib.request.urlopen(urlLink)
parsed = BeautifulSoup(link, 'html.parser')
table = parsed.find('table', attrs={'class': 'wikitable'})
results = table.find_all('tr')

def get_status(row):
    '''
    after analysing the table, we see rowspan is true for outcome and the date in each row
    it was even true for the decay column so I am taking the last result always
    which gives the date and the outcome if present otherwise returns 0
    '''
    division = row.find_all('td', rowspan=True)
    return division[-1].text.strip() if division else 0

def transform(text):
    '''
    given a text like 10 January16:23
    transforms that to - 2019-01-10
    '''
    finalans=""
    for key in codes:
        if(key in text):
            ind  = text.find(key)
            day = text[0:ind-1]
            if(len(day)==1):
                day = "0" + day
            finalans = "2019-" + str(codes[key]) + "-" + day
            return finalans
    return 0

'''
Generate a dictionary with key as all dates in 2019 and value 0
'''
start = datetime.datetime.strptime("2019-01-01", "%Y-%m-%d")
end = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
for date in date_generated:
    ans[date.strftime("%Y-%m-%d")] = 0

codes = {"January":"01","February":"02","March":"03","April":"04","May":"05","June":"06","July":"07","August":"08","September":"09","October":"10","November":"11","December":"12"}


'''
for each line of the result generated, we try to get the date and outcome
if none present, we continue,
if outcome present, and is one of operational or successful or en route,
add it to the map and update count by 1
'''
monthFlag=0
for i in range(len(results)):
    text = (get_status(results[i]))
    if(text==0):
        continue
    if(monthFlag==0):
        dateOfLaunch = transform(text)
        if(dateOfLaunch!=0):
            monthFlag=1
            continue
        else:
            continue
    if(monthFlag==1):
        if("Operational" in text or "Successful" in text or "En Route" in text):
            ans[dateOfLaunch] +=1
            monthFlag=0
            continue
        elif(i+1<len(results)):
            nextLine = get_status(results[i+1])
            while(i+1<len(results) and nextLine==0):
                i=i+1
                nextLine = get_status(results[i+1])
            if(nextLine!=0 and transform(nextLine)!=0):
                monthFlag=0


'''
Lastly, open a csv file - dict.csv, 
add headers of date and value
for each key, value pair in map
update the key as per ISO8601 format
and add the value
'''
with open('Example_output.csv', 'w', newline="") as csv_file:  
    writer = csv.writer(csv_file)
    writer.writerow(['date','value'])
    for key, value in ans.items():
       key = key + "T00:00:00+00:00"
       writer.writerow([key, value])