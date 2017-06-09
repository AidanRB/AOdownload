import requests, getpass, sys
from bs4 import BeautifulSoup

if True:
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
    except NameError:
        print("Warning: the script may crash due to encoding errors on your system.")


username = ""
password = ""

def inputLogin():
    """This function is an easy way to ask the
    user for their username/password.

    It takes no parameters, and defines the
    username and password inside the module
    from input on the terminal.  The password
    is retrieved via getpass, so as to not
    have it in plain text on the terminal.
    """
    global username
    global password
    username = raw_input("Username:\t")
    password = getpass.getpass("Password:\t")

def gatherCredentials():
    """This
    """
    DATA = {
    "url": "https://amblesideonline.org/forum/showthread.php?tid=468",
    "action": "do_login",
    "submit": "Login",
    "quick_login": "1",
    "quick_username": username,
    "quick_password": password,
    }
    global login
    login = (requests.post("https://amblesideonline.org/forum/member.php?action=login", data=DATA))
    if len(BeautifulSoup(login.content, "html.parser").find_all(class_="error")) > 0:
        return False
    else:
        return True

def getPage(tid, pid):
    page = BeautifulSoup(requests.get("https://amblesideonline.org/forum/archive/index.php?thread-" + str(tid) + "-" + str(pid) + ".html", cookies=login.cookies).content, "html.parser")
    pageauthorshtml = page.find_all("div", class_="author")
    pagetimeshtml = page.find_all("div", class_="dateline")
    pagepostshtml = page.find_all("div", class_="message")
    pageauthors = []
    pagetimes = []
    pageposts = []
    for post in zip(pageauthorshtml, pagetimeshtml, pagepostshtml):
        pageauthors.append(post[0].get_text())
        pagetimes.append(post[1].get_text())
        pageposts.append(post[2].get_text())
    return pageauthors, pagetimes, pageposts

def getPages(tid, startpid, endpid):
    startpid
    endpid
    pagesauthors = []
    pagestimes = []
    pagesposts = []
    for currentpagenum in range(endpid - startpid + 1):
        currentpageauthors, currentpagetimes, currentpageposts = getPage(tid, currentpagenum + startpid)
        pagesauthors += currentpageauthors
        pagestimes += currentpagetimes
        pagesposts += currentpageposts
    return pagesauthors, pagestimes, pagesposts

def writeCsv(rows, filename):
    csvfile = open(filename, 'w')
    for row in rows:
        for item in row:
            csvfile.write(item.replace("\n", "\\n") + "\t")
        csvfile.write("\n")


def getResponseData(tid):
    pageBS = BeautifulSoup(requests.post("https://amblesideonline.org/forum/newreply.php?tid=" + str(tid) + "&processed=1", cookies=login.cookies, data={'message': 'don\'t mind me haha'}).content, 'html.parser')
    keyinhtml = pageBS.find(attrs = {"name": "my_post_key"})
    subjectinhtml = pageBS.find(attrs = {"name": "subject"})
    authorarray = pageBS.find_all(class_="smalltext")
    authorarray.pop(-1)
    authorarray.reverse()
    postarray = pageBS.find_all(class_="scaleimages")
    postarray.reverse()
    newaa = []
    newpa = []
    for i in range(len(postarray)):
        newaa.append(authorarray[i].get_text()[10:])
        newpa.append(postarray[i].get_text().split('\n')[1])
    return keyinhtml['value'], subjectinhtml['value'], newaa, newpa

def postReply(postkey, tid, subject, message):          #Returns posted (bool), longenough (bool), secsleft (int)
    postdata = {'my_post_key': postkey, 'submit': 'Post Reply', 'tid': tid, 'action': 'do_newreply', 'message': message, 'subject': subject}
    postsoup = BeautifulSoup(requests.post("https://amblesideonline.org/forum/newreply.php?tid=" + str(tid) + "&processed=1", cookies = login.cookies, data = postdata).content, "html.parser")
    posterrors = postsoup.find(class_="error")
    if posterrors != None:
        posterrors = posterrors.get_text().split('\n')
        if len(posterrors[3]) == 74:
            return False, False, 0
        elif len(posterrors[4]) == 0:
            return False, True, int(posterrors[3][91:93])
        else:
            return False, False, int(posterrors[3][91:93])
    else:
        return True, True, 0
