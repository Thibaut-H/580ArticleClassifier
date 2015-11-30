#!/usr/bin/python2.7
from bs4 import BeautifulSoup
import cgi
import cgitb
import urllib2
import re

#Class for interpreting links passed in to forms
def getArticleWords(url):
	#retrive html from url
	html_Obj = urllib2.urlopen(url).read()
	parsable_Html = BeautifulSoup(html_Obj, "html.parser")

	#identify url type
	agency = getUrlType(url)
	article_Text = getAllText(parsable_Html, agency)

	word_List = []

	for text in article_Text:
		text = text.getText() #get the raw text of each paragraph
		paragraph_List = text.split() #turn each string in words
		for word in paragraph_List: #append each word to the list
			word = re.sub('[^A-Za-z]+', '', word) # remove non-alphanumeric
			if word != '':
				word_List.append(word.lower())

	return word_List

#Returns integer of which agency the url belongs to
# 1  - BBC
# 2  - Huffington Post
# 3  - New York Times
# 4  - The Washington Post
# 5  - CNN
def	getUrlType(url): 
	agency_Name = url[11:] #strip http://www. from url
	abbr = agency_Name[:3]
	if abbr == 'bbc':
		return 1
	if abbr == 'huf':
		return 2
	if abbr == 'nyt':
		return 3
	if abbr == '.wa':
		return 4
	if abbr == 'cnn':
		return 5
	return 0

#Get all of the text for each agency's html structure
def getAllText(parsable_Html, a):
	if(a == 1 or a == 2): #BBC, Huffington Post
		return parsable_Html('p') #find all paragraphs
	if(a == 3): #New York Times
		return parsable_Html.find_all('p', class_="story-body-text")
	if(a == 4): #Washington Post
		article = parsable_Html.find('article')
		return article('p')
	if(a == 5): #CNN
		return parsable_Html.find_all('p', class_="zn-body__paragraph")