import requests
from bs4 import BeautifulSoup
import getpass
import sys
import argparse
from time import sleep
from progress.spinner import Spinner

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    print("While the script may run on your system, it may have escape codes in the result.")

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
    postattempt = requests.post("https://amblesideonline.org/forum/newreply.php?tid=" + str(tid) + "&processed=1", cookies = login.cookies, data = postdata)
    return postattempt

def printHistory(printing):
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
    global lastpost
    lastpost = ap[-1]
    if(printing):
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
    posted = False
    while(not posted):
        printHistory(true)
        prompt = username + " - just now"
        post = raw_input(username + " - just now\n")
        waiting = True
        while(waiting):
            tooshort = True
            attempt = BeautifulSoup(postReply(numtopost, subject, post).content, 'lxml')
            errors = attempt.find(class_='error').find_all('li')
            wait = 0
            if(len(errors) == 2):
                wait = attempt.find(class_='error').find_all('li')[0].get_text()[91:][:2]
            elif(len(errors) == 1):
                if(len(str(errors[0].get_text)) == 114):
                    pass
                else:
                    tooshort = False
                    wait = attempt.find(class_='error').find_all('li')[0].get_text()[91:][:2]
            else:
                tooshort = False
                print("Post successful.")
            print(str(tooshort) + str(wait))
            if(not tooshort and wait == 0):
                posted = True
            elif(wait != 0 and tooshort):
                print("Please wait " + str(wait) + " seconds to post, and your post is too short.")
            elif(wait != 0):
                print("Please wait " + str(wait) + " seconds to post.")
                spiny = Spinner("Posting in ")
                spiny.write(str(wait) + " seconds")
                spiny.start()
                for i in reversed(range(wait)):
                    sleep(1)
                    spiny.next()
                    spiny.write(str(i) + " seconds")
                sleep(1)
                print
                spiny.finish()
            else:
                print("Your post is too short. Must be five or more characters.")
            prevlastpost = lastpost
            printHistory(False)
            if(prevlastpost == lastpost):
                waiting = False
    print("======================\n")
