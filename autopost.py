from PyDictionary import PyDictionary
from contextlib import contextmanager
from bs4 import BeautifulSoup
import requests, getpass, sys, string, os, time

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    print("Warning: the script may crash due to encoding errors on your system.")

username = raw_input("Username:\t")
password = getpass.getpass("Password:\t")
threadnum = 468
avoid468 = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \n'
synant = True

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

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

def getHistory():
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
    return newaa[-1], str(newpa[-1]).translate(string.maketrans("",""), avoid468).lower()

def autopost(lastp):
    global synant
    with suppress_stdout():
        if(synant):
            syns = syn(lastp)
            synant = False
        else:
            syns = ant(lastp)
            synant = True
        if(syns == None):
            means = meaning(lastp)

    if(syns != None):
        postraw = syns[0]
    elif(means == None):
        postraw = "what XD\nI'm just a bot!  I can't understand that!"
    else:
        wordtype, wordmeans = means.items()[0]
        postraw = wordtype

    firstletter = postraw[0].upper()
    postword = firstletter + postraw[1:]
    postword = postword.ljust(4) + '.'
    print("Replying with " + postword + "..")
    postReply(468, "Autoposted", postword)
    print("Replied!")

syn = PyDictionary.synonym
ant = PyDictionary.antonym
meaning = PyDictionary.meaning

login = gatherCookieJar()

while(True):
    postkey, subject = getPostKey(threadnum)

    lasta, lastp = getHistory()

    userlen = len(username)

    print("###")

    if(username.lower() != lasta[:userlen].lower()):
        print("\n" + lasta + " - " + lastp)
        autopost(lastp)
        time.sleep(30)

    time.sleep(30)