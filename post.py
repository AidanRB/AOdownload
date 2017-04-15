import requests
import getpass
from bs4 import BeautifulSoup
import argparse
import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    print("Warning: the script may crash due to encoding errors on your system.")

try:
    parser = argparse.ArgumentParser(description="Posts to the Ambleside Online forum.  More information can be found at https://goo.gl/L88u48")
    parser.add_argument("thread", help="Thread ID to post to (number)", type=int)
    parser.add_argument("username", help="User to post from")
    args = parser.parse_args()
    threadnum = args.thread
    username = args.username
except:
    print("You messed something up; entering interactive mode.\n")
    threadnum = input("Thread number:\t")
    username = raw_input("Username:\t")
password = getpass.getpass("Password:\t")
print

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
    return login

def getPostKey(tid):
    global pageBS
    pageraw = requests.post("https://amblesideonline.org/forum/newreply.php?tid=" + str(tid) + "&processed=1", cookies=login.cookies, data={'message': 'don\'t mind me haha'})
    pageBS = BeautifulSoup(pageraw.content, 'html.parser')
    keyinhtml = pageBS.find(attrs = {"name": "my_post_key"})
    subjectinhtml = pageBS.find(attrs = {"name": "subject"})
    return keyinhtml['value'], subjectinhtml['value']

def postReply(tid, subject, message):
    postdata = {'my_post_key': postkey, 'submit': 'Post Reply', 'tid': tid, 'action': 'do_newreply', 'message': message.replace("\\n", "\n"), 'subject': subject}
    requests.post("https://amblesideonline.org/forum/newreply.php?tid=" + str(tid) + "&processed=1", cookies = login.cookies, data = postdata)

def printHistory():
    historyBS = BeautifulSoup(str(pageBS.find(class_="tborder tfixed")), 'html.parser')

    authorarray = historyBS.find_all(class_="smalltext")
    authorarray.pop(-1)
    authorarray.reverse()
    postarray = historyBS.find_all(class_="scaleimages")
    postarray.reverse()

    newaa = []
    newpa = []
    for i in range(len(authorarray)):
        newaa.append(authorarray[i].get_text()[10:])
        newpa.append(postarray[i].get_text().split('\n')[1])
    aparray = zip(newaa, newpa)

    global columnwidth
    columnwidth = max(len(author) for author in newaa) + 4
    for ap in aparray:
        print (ap[0].ljust(columnwidth) + ap[1])
        print

login = gatherCookieJar()

postkey, subject = getPostKey(threadnum)

printHistory()

prompt = username + " - just now"
post = raw_input(prompt.ljust(columnwidth))

postReply(threadnum, subject, post)
