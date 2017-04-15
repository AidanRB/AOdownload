import requests
from bs4 import BeautifulSoup
import getpass
import sys
import argparse

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    print("While the script may download on your system, it may have escape codes in the result.")

username = raw_input("Username:\t")
password = getpass.getpass()

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

def subToSoup(cookies, pnum):
    return BeautifulSoup(requests.get("https://amblesideonline.org/forum/usercp.php?action=subscriptions&page=" + str(pnum), cookies = cookies).content, "html.parser")

def extractTnP(pageBS):
    threads = pageBS.find_all(class_=["subject_old", "subject_new"])
    tnames = []
    tnums = []
    noro = []
    for thread in threads:
        tnames.append(thread.get_text())
        tnums.append(thread['href'][19:])
        noro.append(thread['class'][0][8:])
    tposters = []
    """for thread in pageBS.select("table.tborder"):
        tposters.append(thread.select("tr")[4].select("td")[5].select("a")[1].get_text())"""
    return tnames, tnums, noro, tposters

def printSubs(threads):
    #cw = max(len(num) for num in tnums) + 2
    i = 0
    for thread in threads:
        i+=1
        print((str(i) + ".").ljust(4) + thread[1] + " - " + thread[0] + ":")

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
        post = postarray[i].get_text().split('\n')
        post.pop(0)
        post.pop(-1)
        poststr = ""
        for line in post:
            poststr = poststr + "\n" + line
        newpa.append(poststr)
    aparray = zip(newaa, newpa)
    global columnwidth
    columnwidth = max(len(author) for author in newaa) + 4
    for ap in aparray:
        print(ap[0].ljust(columnwidth) + ap[1])
        print("======================")

login = gatherCookieJar()

while True:
    pageBS = subToSoup(login.cookies, 1)
    tnames, tnums, noro, tposters = extractTnP(pageBS)
    threads = zip(tnames, noro, tnums)
    print("Subscriptions:")
    printSubs(threads)
    numtopost = threads[input("Thread number:") - 1][2]
    postkey, subject = getPostKey(numtopost)
    printHistory()
    prompt = username + " - just now"
    post = raw_input(username + " - just now\n")
    postReply(numtopost, subject, post)
    print("======================\n")
