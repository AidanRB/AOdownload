import requests
import getpass
from bs4 import BeautifulSoup

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
    login = (requests.post("https://amblesideonline.org/forum/member.php?action=login", data=DATA))
    print("Login complete")
    return login

def getPostKey(tid):
    pageraw = requests.post("https://amblesideonline.org/forum/newreply.php?tid=" + str(tid) + "&processed=1", cookies=login.cookies, data={'message': 'don\'t mind me haha'})
    pageBS = BeautifulSoup(pageraw.content, 'html.parser')
    keyinhtml = pageBS.find(attrs = {"name": "my_post_key"})
    return keyinhtml['value']

def postReply(tid, subject, message):
    postdata = {'my_post_key': postkey, 'submit': 'Post Reply', 'tid': tid, 'action': 'do_newreply', 'message': message, 'subject': subject}
    requests.post("https://amblesideonline.org/forum/newreply.php?tid=" + str(tid) + "&processed=1", cookies = login.cookies, data = postdata)

login = gatherCookieJar()

threadnum = input("Thread number:\t")
subject = raw_input("Post subject:\t")
post = raw_input("Your message:\t")

postkey = getPostKey(threadnum)
postReply(threadnum, subject, post)
