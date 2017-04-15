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

def subToSoup(cookies):
    return BeautifulSoup(requests.get("https://amblesideonline.org/forum/usercp.php?action=subscriptions", cookies = cookies))

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
    for thread in pageBS.select("table.tborder"):
        tposters.append(thread.select("tr")[4].select("td")[5].select("a")[1].get_text())
    return tnames, tnums, noro, tposters

login = gatherCookieJar()

pageBS = subToSoup(login.cookies)

tnames, tnums, noro, tposters = extractTnP(pageBS)

print(tnames)
print(tnums)
print(noro)
print(tposters)
