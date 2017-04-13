import requests
import getpass
from bs4 import BeautifulSoup
import argparse


try:
    parser = argparse.ArgumentParser(description="Posts to the Ambleside Online forum.  More information can be found at https://goo.gl/L88u48")
    parser.add_argument("thread", help="Thread ID to post to (number)", type=int)
    parser.add_argument("subject", help="Post subject")
    parser.add_argument("message", help="Post content")
    parser.add_argument("username", help="User to post from")
    args = parser.parse_args()
    threadnum = args.thread
    post = args.message
    username = args.username
    subject = args.subject
except:
    print("You messed something up; entering interactive mode:\n")
    threadnum = input("Thread number:\t")
    subject = raw_input("Post subject:\t")
    post = raw_input("Your message:\t")
    username = raw_input("Username:\t")
password = getpass.getpass("Password:\t")


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
    pageraw = requests.post("https://amblesideonline.org/forum/newreply.php?tid=" + str(tid) + "&processed=1", cookies=login.cookies, data={'message': 'don\'t mind me haha'})
    pageBS = BeautifulSoup(pageraw.content, 'html.parser')
    keyinhtml = pageBS.find(attrs = {"name": "my_post_key"})
    return keyinhtml['value']

def postReply(tid, subject, message):
    postdata = {'my_post_key': postkey, 'submit': 'Post Reply', 'tid': tid, 'action': 'do_newreply', 'message': message, 'subject': subject}
    requests.post("https://amblesideonline.org/forum/newreply.php?tid=" + str(tid) + "&processed=1", cookies = login.cookies, data = postdata)

login = gatherCookieJar()

postkey = getPostKey(threadnum)
postReply(threadnum, subject, post)
