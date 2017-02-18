import requests
from bs4 import BeautifulSoup
import re
import time
import os
import getpass

threadnumber = input("What thread?\t")
firstpage = input("First page:\t")
lastpage = input("Last page:\t")

def gatherCookieJar():
    DATA = {  #Data for logging in.
    "url": "https://amblesideonline.org/forum/showthread.php?tid=468",
    "action": "do_login",
    "submit": "Login",
    "quick_login": "1",
    "quick_username": raw_input("Username:\t"),
    "quick_password": getpass.getpass("Password:\t"),
    }

    global login
    login = (requests.post("https://amblesideonline.org/forum/member.php?action=login", data=DATA))  #Gathers cookies nessecary for login.

    print("Login complete")
    return login

def getPage(tid, pid):
    global page
    page = BeautifulSoup(requests.get("https://amblesideonline.org/forum/archive/index.php?thread-" + str(tid) + "-" + str(pid) + ".html", cookies=login.cookies).content)

def getAuthors1Page():
    global authors
    authors = page.find_all("div", class_="author")

def getTimes1Page():
    global times
    times = page.find_all("div", class_="dateline")

def getPosts1Page():
    global posts
    posts = page.find_all("div", class_="message")

def print1Page():
    for i in range(len(authors)):
        print("Post #" + str(pagenumber * 10 + i) + ":  " + authors[i].get_text() + " posted at " + times[i].get_text() + ":\n" + posts[i].get_text() + "\n\n")

def csvOpen():
    global csv
    csv = open("thread" + str(threadnumber) + "pages" + str(firstpage) + "-" + str(lastpage) + ".csv", 'w')

def csv1Page():
    for i in range(len(authors)):
        csv.write(str(pagenumber * 10 + i) + "\t" + times[i].get_text() + "\t" + authors[i].get_text() + "\t" + posts[i].get_text() + "\n")

def csvMultiPage():
    csvOpen()
    for i in range(lastpage - firstpage + 1):
        print(i)
