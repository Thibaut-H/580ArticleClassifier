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

#Get words from each url and count in dictionary
for i in range(0,20):
	formId = 'urlForm' + str(i)
	article_Url = form.getvalue(formId)
	if article_Url: #If a URL was input into particular field
		word_List = urlParser.getArticleWords(article_Url);
		if word_List: #If anything was actually retrieved
			for word in word_List:
				if word in word_Counter: #Faster than 'not word in word_Counter'
					word_Counter[word] += 1
				else:
					word_Counter[word] = 1
			urlsAdded += 1

#Remove common words
cwl = [] #Common words list
with open('common_words.txt', 'r') as f:
	for line in f:
		cwl.append(line.rstrip('\n'))

for word in cwl:
	if word in word_Counter:
		del word_Counter[word]

#Augment training file
#Create dictionary of current words in classification file
cFilename = aType + '.txt' #Classification filename
totalUrls = 0 #Size of training set
fileDict = {}
with open(cFilename, 'a+') as f:
	f.seek(0)
	totalUrls = f.readline() + str(urlsAdded) #Url total on first line
	for line in f:
		w = line.split()
		fileDict[w[0]] = w[1]

#Augment or add to dict
for word in word_Counter:
	if word in fileDict:
		fileDict[word] += word_Counter[word]
	else:
		fileDict[word] = word_Counter[word]

with open(cFilename, 'w+') as f:
	f.write(str(totalUrls) + '\n')
	for word in fileDict:
		f.write(word + ' ' + str(fileDict[word]) + '\n')

print "Content-type: text/html"
print
print "<html><body>"
print "Successfully added " + str(urlsAdded) + " Urls to training data for \'" + aType + "\'<br>"
print str(totalUrls) + " total Urls\n"
print str(len(word_Counter)) + " total words"
# for word in fileDict:
# 	print word + '<br>'
print "</html><body>"