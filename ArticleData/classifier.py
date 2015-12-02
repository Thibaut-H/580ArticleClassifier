#!/usr/bin/python2.7
import cgi
import cgitb
import urllib2
import glob
import urlParser
import nbn_prob

#enable debugging
cgitb.enable()

#retrieve url form input
form = cgi.FieldStorage()
article_Url = form.getvalue('urlForm')

word_List = urlParser.getArticleWords(article_Url)

#add script to parse the url of urls
# page with links to all other articles: http://feeds.bbci.co.uk/news/rss.xml

#retrieve most common words for extraction
cwl = [] #common words list
with open('.common_words.txt', 'r') as f:
	for line in f:
		cwl.append(line.rstrip('\n'))

#Sort List for easy counting
word_List.sort()
word_Counter = {}
prev_Word = ""
for word in word_List:
	if prev_Word != word: #Faster than 'not word in word_Counter'
		word_Counter[word.rstrip('\n')] = 1
		prev_Word = word
	else:
		word_Counter[word.rstrip('\n')] += 1
 # #Add check to known key words

for word in cwl:
	if word in word_Counter:
		del word_Counter[word]

#Iterate through all classification files
#Pull name using string splitting
dictList = [] #what
namesList = []
numUrlsList = []

allClassNames = glob.glob('*.txt') #Get list of class files
for className in allClassNames:
	if className[0] != '.': #Exclude URL files
		fileDict = {}
		with open(className, 'r') as f:
			tmp = f.readline().split()
			namesList.append(tmp[0]) #Classification name
			numUrlsList.append(int(tmp[1])) #Number of urls aggregated
			for line in f:
				w = line.split()
				fileDict[w[0]] = int(w[1])
			dictList.append(fileDict)

allProbs = nbn_prob.calc_probs(word_Counter, dictList, numUrlsList, 1)


print "Content-type: text/html"
print
print "<html><body>"
for name in namesList:
	print str(numUrlsList) + '<br>'
for i in range(0,len(namesList)):
	print namesList[i] + ' - ' + str(allProbs[i]) +  '<br>'
#for word in word_Counter:
#	print ( str(word_Counter[word]) + '-' + word +"<br>")
print "</body></html>"