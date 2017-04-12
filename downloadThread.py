import requests
from bs4 import BeautifulSoup
import getpass
import sys
import argparse

#Set encoding to utf8 so we don't have weird problems with odd characters
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    print("While the script may download on your system, it may have escape codes in the result.")

try:
    parser = argparse.ArgumentParser(description="Download a thread from the AO forums. More information can be found at https://goo.gl/L88u48")
    parser.add_argument("thread", help="Thread ID to download (number)", type=int)
    parser.add_argument("first", help="Page on which to start downloading", type=int)
    parser.add_argument("last", help="Page on which to stop downloading", type=int)
    parser.add_argument("username", help="Username to authenticate with")
    parser.add_argument("out", help="Output type: Txt, Csv, or Print (on terminal)")
    parser.add_argument("--ppp", help="Custom posts per page; for use if you have a custom set.", type=int, default=10)

    args = parser.parse_args()

    threadnumber = args.thread
    firstpage = args.first
    lastpage = args.last
    ppp = args.ppp
    type = args.out.lower()
    username = args.username
except:
    print("You messed something up; entering interactive mode:\n")

    threadnumber = int(input("Thread: "))
    firstpage = int(input("First page: "))
    lastpage = int(input("Last page: "))
    ppp = int(input("Posts per page (usually 10): "))
    type = raw_input("Output type: ").lower()
    username = raw_input("Username: ")

password = getpass.getpass("Password:\t")
#Gather input about the data to be downloaded
"""threadnumber = input("What thread?\t")
firstpage = input("First page:\t")
lastpage = input("Last page:\t")"""

#Gathers login information
def gatherCookieJar():
    DATA = {  #Data for logging in.
    "url": "https://amblesideonline.org/forum/showthread.php?tid=468",
    "action": "do_login",
    "submit": "Login",
    "quick_login": "1",
    "quick_username": username,
    "quick_password": password,
    }
    global login
    login = (requests.post("https://amblesideonline.org/forum/member.php?action=login", data=DATA))
    print("Login complete")
    return login

#Loads one page into RAM as a BeautifulSoup object
def getPage(tid, pid):
    global page
    page = BeautifulSoup(requests.get("https://amblesideonline.org/forum/archive/index.php?thread-" + str(tid) + "-" + str(pid) + ".html", cookies=login.cookies).content, "html.parser")

#Pulls the authors out of the loaded page
def getAuthors1Page():
    global authors
    authors = page.find_all("div", class_="author")

#Pulls the times out of the loaded page
def getTimes1Page():
    global times
    times = page.find_all("div", class_="dateline")

#Pulls the posts out of the loaded page
def getPosts1Page():
    global posts
    posts = page.find_all("div", class_="message")

#Loads and parses one page
def getAll1Page(pid):
    getPage(threadnumber, pid)
    getPosts1Page()
    getAuthors1Page()
    getTimes1Page()

#Prints one page on the terminal
def print1Page():
    for i in range(len(authors)):
        print("Post #" + str(pagenumber * ppp + i + 1) + ":  " + authors[i].get_text() + " posted at " + times[i].get_text() + ":\n" + posts[i].get_text() + "\n\n")

#Prints all requested pages to the terminal
def printMultiPage():
    global pagenumber
    for pagenumber in range(lastpage - firstpage + 1):
        print("Downloading page " + str(pagenumber + 1))
        getAll1Page(firstpage + pagenumber)
        print1Page()

#Opens a CSV file for writing
def csvOpen():
    global csv
    csv = open("thread" + str(threadnumber) + "pages" + str(firstpage) + "-" + str(lastpage) + ".csv", 'w')

#Writes one page of posts to the opened CSV, using tab as seperator
def csv1Page():
    for i in range(len(authors)):
        csv.write(times[i].get_text() + "\t" + authors[i].get_text() + "\t" + posts[i].get_text() + "\n")

#Writes all requested pages to the opened CSV
def csvMultiPage():
    csvOpen()
    global pagenumber
    for pagenumber in range(lastpage - firstpage + 1):
        print("Downloading page " + str(pagenumber + 1))
        getAll1Page(firstpage + pagenumber)
        csv1Page()

#Opens a text file for writing
def txtOpen():
    global txt
    txt = open("thread" + str(threadnumber) + "pages" + str(firstpage) + "-" + str(lastpage) + ".txt", 'w')

def txt1Page():
    for i in range(len(authors)):
        txt.write("Post #" + str(pagenumber * ppp + i + 1) + ":  " + authors[i].get_text() + " posted at " + times[i].get_text() + ":\n" + posts[i].get_text() + "\n\n")

#Writes all requested pages to a text file
def txtMultiPage():
    txtOpen()
    global pagenumber
    for pagenumber in range(lastpage - firstpage + 1):
        print("Downloading page " + str(pagenumber + 1))
        getAll1Page(firstpage + pagenumber)
        txt1Page()

#Logs in
gatherCookieJar()

#Asks what kind of file to write to
if(type == "txt" or type == "text" or type == "t" or type == "1"):
    txtMultiPage()
elif(type == "csv" or type == "c" or type == "2"):
    csvMultiPage()
elif(type == "print" or type == "p" or type == "3"):
    printMultiPage()
