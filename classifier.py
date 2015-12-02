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

#retrieve most common words for extraction
cwl = [] #common words list
with open('.common_words.txt', 'r') as f:
	for line in f:
		cwl.append(line.rstrip('\n'))

word_List.sort() #Sort List for easy counting
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
dictList = []
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
print "<html>"
print "	<link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>"
print " <link href='https://fonts.googleapis.com/css?family=Pacifico' rel='stylesheet' type='text/css'>"
print "<style>body{font-family:'Roboto',sans-serif;}"
print "h2{font-family: 'Pacifico', cursive;margin-left: 40px}</style>"
print "<body>"
print "<h2>Probabilities</h2><br>"
for i in range(0,len(namesList)):
	print "<b>" + namesList[i] + "</b><ul>  " + str(allProbs[i]) + "</ul>"
print "<br><br>Your article type is " + namesList[allProbs.index(max(allProbs))].lower()
print "</body></html>"