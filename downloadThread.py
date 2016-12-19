import requests
from bs4 import BeautifulSoup
import re
import time
import os
import getpass

#author: td class="post_author"
#post:   div class="post_body"
#date:   div class="float_left smalltext"

#If you have problems, make sure requests is installed.  http://docs.python-requests.org/en/master/

def gatherCookieJar():
	DATA = {		#Data for logging in.
	"url": "https://amblesideonline.org/forum/showthread.php?tid=468",
	"action": "do_login",
	"submit": "Login",
	"quick_login": "1",
	"quick_username": raw_input("Username:\t"),
	"quick_password": getpass.getpass("Password:\t"),
	}

	login = (requests.post("https://amblesideonline.org/forum/member.php?action=login", data=DATA))		#Gathers cookies nessecary for login.

	print("Login complete")

	return login

def getPage(tid, pagenumber):
	page = requests.get("https://amblesideonline.org/forum/showthread.php?tid=" + str(tid) + "&page=" + str(pagenumber), cookies=login.cookies)

	return page

def savePage(tid, pagenumber):
	pagefile = open("thread" + str(tid) + "page" + str(pagenumber) + ".html", "w")

	page = getPage(tid, pagenumber)

	pagefile.write(page.content)

	print("Page " + str(pagenumber) + " downloaded.")

	pagefile.close()

def savePages(tid, startpage, pages):
	for i in range(pages):
		savePage(tid, startpage + i)

def openToParse(tid, page):
	parsingf = open("thread" + str(tid) + "page" + str(page) + ".html", "r")
	global psoup
	psoup = BeautifulSoup(parsingf.read(), 'html.parser')
	global soupwf

def getPosts1Page():
	postsoup = BeautifulSoup(str(psoup.find_all("div", class_="post_body")), 'lxml')
	return postsoup

def getAuthors1Page():
	authors = psoup.find_all("td", class_="post_author")
	authorsoup = BeautifulSoup(str(authors), 'lxml')
	authorarray = authorsoup.get_text()
	authorarray = authorarray.split(',')
	return authorarray

def getTimes1Page():
	timesoup = BeautifulSoup(str(psoup.find_all("div", class_="float_left smalltext")), 'lxml')
	return timesoup

def printStuff():
	for j in range(10):
		time = re.sub('\\\\r|\\\\t|\\\\n', '', times.find_all("div")[j].get_text())		# oh my backslash
		#author = str(authors.find_all("strong")[j].get_text())
		print("At " + time + re.sub('\\\\n', '', re.search('\\\\n.*\\\\n\\\\n\\\\n', authors[j]).group(0)) + " wrote:")
		print("")
		print(re.sub('\\\\n', '\n', re.sub('\\\\t|\\\\r', '', posts.find_all("div")[j].get_text())))
		print("__________________________________________________________________________________________")
		print("")

def printStuffPages(tid, pagenumber, pages):
	for i in range(pages):
		openToParse(tid, pagenumber + i)
		global posts
		global authors
		global times
		posts = getPosts1Page()
		authors = getAuthors1Page()
		times = getTimes1Page()
		printStuff()

def writePage():
	for j in range(10):
		time = re.sub('\\\\r|\\\\t|\\\\n', '', times.find_all("div")[j].get_text())		# oh my backslash
		author = re.sub('\\\\n', '', re.search('\\\\n.*\\\\n\\\\n\\\\n', authors[j]).group(0))
		post = re.sub('\\\\t|\\\\r', '', posts.find_all("div")[j].get_text())

		writef.write(time + "\t" + author + "\t" + post + "\n")

def writeThread(tid, pagenumber, pages):
	global writef
	writef = open(str(tid) + "pages" + str(pagenumber) + "-" + str(pagenumber + pages - 1) + "___" + str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + "." + str(time.localtime()[5]) + "___" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]) + "-" + str(time.localtime()[0]) + ".csv", 'a')
	for i in range(pages):
		openToParse(tid, pagenumber + i)
		global posts
		global authors
		global times
		posts = getPosts1Page()
		authors = getAuthors1Page()
		times = getTimes1Page()
		writePage()
		print("Page " + str(pagenumber + i) + " inserted.")

def writePageCustom():
	for j in range(10):
		time = re.sub('\\\\r|\\\\t|\\\\n', '', times.find_all("div")[j].get_text())		# oh my backslash
		author = re.sub('\\\\n', '', re.search('\\\\n.*\\\\n\\\\n\\\\n', authors[j]).group(0))
		post = re.sub('\\\\n', '\n', re.sub('\\\\t|\\\\r', '', posts.find_all("div")[j].get_text()))

		writef.write("        At " + time + author + " wrote:\n" + post + "\n________________________________________________________________________________________________________________\n\n\n")

def writeThreadCustom(tid, pagenumber, pages, filename):
	global writef
	writef = open(str(filename) + ".txt", 'a')
	for i in range(pages):
		openToParse(tid, pagenumber + i)
		global posts
		global authors
		global times
		posts = getPosts1Page()
		authors = getAuthors1Page()
		times = getTimes1Page()
		writePageCustom()
		print("Page " + str(pagenumber + i) + " inserted.")

def writePageWA():
	for j in range(10):
		time = re.sub('\\\\r|\\\\t|\\\\n', '', times.find_all("div")[j].get_text())		# oh my backslash
		author = re.sub('\\\\n', '', re.search('\\\\n.*\\\\n\\\\n\\\\n', authors[j]).group(0))
		post = re.sub('\\\\t|\\\\r', '', posts.find_all("div")[j].get_text())
		post = re.sub('\\\\n/^(.*?)\\\\n/', "The post was here", post)

		post = post.split(" ")

		post = post[0].split("\\n")

		writef.write(time + "\t" + author + "\t" + post[0] + "\n")

def writeThreadWA(tid, pagenumber, pages, filename):
	global writef
	writef = open(str(filename) + ".csv", 'a')
	for i in range(pages):
		openToParse(tid, pagenumber + i)
		global posts
		global authors
		global times
		posts = getPosts1Page()
		authors = getAuthors1Page()
		times = getTimes1Page()
		writePageWA()
		print("Page " + str(pagenumber + i) + " inserted.")

def cleanUp(tid, pagenumber, pages):
	for i in range(pages):
		os.remove("thread" + str(tid) + "page" + str(i + pagenumber) + ".html")

global login
login = gatherCookieJar()

global posts
global authors
global times

print("| Word association | 468   |")
print("| Impromptu        | 15444 |")

threadnum = int(raw_input("What thread do you want to download?       "))
pagenum = int(raw_input("What page should be the first one?         "))
pagerange = int(raw_input("How many pages do you want downloaded?     "))

print("Downloading " + str(pagerange) + " pages of thread " + str(threadnum) + " starting at page " + str(pagenum) + ".")

			##  ---END DEFINITIONS--- ##

savePages(threadnum, pagenum, pagerange)

print("\n\n\n------------------------ Downloading complete. ------------------------\n\n\n")

towriteornottowrite = raw_input("Do you want the thread in a .CSV/spreadsheet (seperator is tab)?  y/N:  ")
if(towriteornottowrite == 'Y' or towriteornottowrite == 'y'):
	writeThread(threadnum, pagenum, pagerange)

toprintornottoprint = raw_input("Do you want to see the thread here?  y/N:  ")
if(toprintornottoprint == "Y" or toprintornottoprint == "y"):
	printStuffPages(threadnum, pagenum, pagerange)

towritecustomornottowritecustom = raw_input("Do you want the thread written to an easily readable/editable text file?  y/N:  ")
if(towritecustomornottowritecustom == "Y" or towritecustomornottowritecustom == "y"):
	writeThreadCustom(threadnum, pagenum, pagerange, str(raw_input("What should the file be called?  ")))

if(threadnum == 468 or threadnum == 19185):
	waconfirm = raw_input("Do you want the first word in each post in a file?  y/N:  ")
	if(waconfirm == "Y" or waconfirm == "y"):
		writeThreadWA(threadnum, pagenum, pagerange, str(raw_input("What should the file be called?  ")))


cleanUpOrNot = raw_input("Should I clean up all the HTML files?  Y/n:  ")
if(cleanUpOrNot != "N" and cleanUpOrNot != "n"):
	cleanUp(threadnum, pagenum, pagerange)

print("Done.")
