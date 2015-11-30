#!/usr/bin/python2.7
import cgi
import cgitb
import urllib2
import urlParser

#enable debugging
cgitb.enable()

#retrieve url form input
form = cgi.FieldStorage()
article_Url = form.getvalue('urlForm')

word_List = urlParser.getArticleWords(article_Url);

#add script to parse the url of urls
# page with links to all other articles: http://feeds.bbci.co.uk/news/rss.xml

#retrieve most common words for extraction
cwl = [] #common words list
with open('common_words.txt', 'r') as f:
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

print "Content-type: text/html"
print
print "<html><body>"
for word in word_Counter:
	print ( str(word_Counter[word]) + '-' + word +"<br>")
print "</body></html>"