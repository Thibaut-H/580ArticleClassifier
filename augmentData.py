#!/usr/bin/python2.7
import cgi
import cgitb
import urllib2
import urlParser

#enable debugging
cgitb.enable()

#retrieve all urls from input data
urlsAdded = 0
word_Counter = {} #Aggregate of all URLs input
form = cgi.FieldStorage()

aType = form.getvalue('tagName') #Article Type
cUrlFilename = '.' + aType.lower() + 'Urls.txt' #Storage of urls to prevent duplicates
urlList = []

#Retrieve list of previously added urls / Create file
with open(cUrlFilename, 'a+') as f:
	f.seek(0)
	for line in f:
		urlList.append(line.rstrip('\n'))

#Get words from each url and count in dictionary
for i in range(0,10):
	formId = 'urlForm' + str(i)
	article_Url = form.getvalue(formId)
	if article_Url: #If a URL was input into particular field
		if article_Url not in urlList: #Prevent duplicate Urls from being added
			word_List = urlParser.getArticleWords(article_Url);
			if word_List: #If anything was actually retrieved
				urlList.append(article_Url)
				for word in word_List:
					if word in word_Counter: #Faster than '~ word in word_Counter'
						word_Counter[word] += 1
					else:
						word_Counter[word] = 1
				urlsAdded += 1

#Write new urls to file
with open(cUrlFilename, 'w+') as f:
	for url in urlList:
		f.write(url + '\n')

#Remove common words
cwl = [] #Common words list
with open('.common_words.txt', 'r') as f:
	for line in f:
		cwl.append(line.rstrip('\n'))

for word in cwl:
	if word in word_Counter:
		del word_Counter[word]

#Augment training file
#Create dictionary of current words in classification file
cFilename = aType.lower() + '.txt' #Classification filename
totalUrls = 0 #Size of training set
fileDict = {}

#Read/Create training file
with open(cFilename, 'a+') as f:
	f.seek(0)
	l = f.readline().split() #Url total on first line
	if l:
		totalUrls = int(l[1])
		for line in f:
			w = line.split()
			fileDict[w[0]] = int(w[1])

totalUrls += urlsAdded #Update totalUrls

#Augment or add to dict
for word in word_Counter:
	if word in fileDict:
		fileDict[word] += word_Counter[word]
	else:
		fileDict[word] = word_Counter[word]

with open(cFilename, 'w+') as f:
	f.write(aType + ' ' + str(totalUrls) + '\n');#tag name, total urls counted
	for word in fileDict:
		f.write(word + ' ' + str(fileDict[word]) + '\n')


print "Content-type: text/html"
print
print "<html>"
print "	<link href='https://fonts.googleapis.com/css?family=Roboto' " +"rel='stylesheet' type='text/css'>"
print "<style>body{font-family:'Roboto',sans-serif;}</style>"
print "<body>"
print "Successfully added " + str(urlsAdded) + " Urls to training data for \'"+aType + "\'<br>"
print str(totalUrls) + " total Urls<br>"
print str(len(fileDict) - 1) + " total words<br>"
print "<br>Current words in File<br><br>"
for word in fileDict:
	print word + " " + str(fileDict[word]) + "<br>"
print "</body></html>"