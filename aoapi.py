"""Unofficial third-party API for interacting with the AO forums."""

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
postkey = ""

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
    """This function logs the user into the forum;
    ie; it retrieves their cookies.

    NOTE: inputLogin() or some other method of
    retrieving user/pass MUST be executed FIRST.
    This does NOT ask for user/pass.

    Returns True if succeeded, False if failed.
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
    global postkey
    login = (requests.post("https://amblesideonline.org/forum/member.php?action=login", data=DATA))
    if len(BeautifulSoup(login.content, "html.parser").find_all(class_="error")) > 0:
        return False
    else:
        keyBS = BeautifulSoup(requests.post("https://amblesideonline.org/forum/newreply.php?tid=11467&processed=1", cookies=login.cookies, data={'message': 'don\'t mind me haha'}).content, 'html.parser')
        postkey = keyBS.find(attrs = {"name": "my_post_key"})['value']
        return True

def logout():
    try:
        global username
        global password
        global postkey
        global login
        username = ""
        password = ""
        postkey = ""
        del login
    except:
        pass

def getPage(tid, pid):
    """This function retrieves one page of posts.

    Parameters are threadnumber, pagenumber.
    This can be retrieved from the URL of the
    page or through another command.

    Returns authors[], times[], posts[], threadname,
    pages, navtitles, navthreadnums.
    """
    try:
        login
    except NameError:
        page = BeautifulSoup(requests.get("https://amblesideonline.org/forum/archive/index.php?thread-" + str(tid) + "-" + str(pid) + ".html").content, "html.parser")
    else:
        page = BeautifulSoup(requests.get("https://amblesideonline.org/forum/archive/index.php?thread-" + str(tid) + "-" + str(pid) + ".html", cookies=login.cookies).content, "html.parser")
    if(page.find_all("div", class_="error") != []):
        return False
    pageauthorshtml = page.find_all("div", class_="author")
    pagetimeshtml = page.find_all("div", class_="dateline")
    pagepostshtml = page.find_all("div", class_="message")
    pagetitle = page.find_all("title")
    pageauthors = []
    pagetimes = []
    pageposts = []
    for post in zip(pageauthorshtml, pagetimeshtml, pagepostshtml):
        pageauthors.append(post[0].get_text())
        pagetimes.append(post[1].get_text())
        pageposts.append(str(post[2])[21:-6])
    try:
        pages = page.find_all(class_="multipage")[0].get_text().split(" ")[-2]
    except:
        pages = 1
    navigation = page.find_all(class_="navigation")[0]
    navigators = navigation.find_all("a")
    navigators.pop(0)
    navtitles = []
    navnums = []
    for navigator in navigators:
        navtitles.append(navigator.get_text())
        navnums.append(int(navigator.get("href")[58:-5]))
    return pageauthors, pagetimes, pageposts, pagetitle[0].get_text().split("-")[1][1:], pages, navtitles, navnums

def getPages(tid, startpid, endpid):
    """This function makes retrieval of multiple
    pages easier, by repeatedly calling
    getPage() and stitching the results
    together.

    Parameters are threadnumber, startpage,
    endpage.  This can be retrieved from the
    URL of the page or through another command.

    Returns authors[], times[], posts[], threadname,
    pages, navtitles, navthreadnums.
    """
    title = ""
    pagesauthors = []
    pagestimes = []
    pagesposts = []
    try:
        for currentpagenum in range(endpid - startpid + 1):
            currentpageauthors, currentpagetimes, currentpageposts, title, pages, navtitles, navnums = getPage(tid, currentpagenum + startpid)
            pagesauthors += currentpageauthors
            pagestimes += currentpagetimes
            pagesposts += currentpageposts
    except:
        return False
    return pagesauthors, pagestimes, pagesposts, title, pages, navtitles, navnums

def writeCsv(rows, filename):
    """This function writes given data to a CSV.

    Format is (["Item 1 row 2", "Item 2 row 1"]
               ["Item 1 row 2", "Item 2 row 2"])
    This can be easily obtained with output from getPage:
        zip(output[0], output[1], output[2])
        in the format author, date, post (columns).

    Parameters are rows (nested arrays), filename.
    """
    csvfile = open(filename, 'w')
    for row in rows:
        for item in row:
            csvfile.write(item.replace("\n", "\\n") + "\t")
        csvfile.write("\n")

def getResponseData(tid):
    """This function gathers the data necessary to
    respond to a thread, as well as the last ten posts.

    The only parameter is the threadnumber.  It returns
    subject (passed to postReply()) authors[] (last ten),
    posts[] (last ten).
    """
    global postkey
    if (postkey == ""):
        return False
    pageBS = BeautifulSoup(requests.post("https://amblesideonline.org/forum/newreply.php?tid=" + str(tid) + "&processed=1", cookies=login.cookies, data={'message': 'don\'t mind me haha'}).content, 'html.parser')
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
    return subjectinhtml['value'], newaa, newpa

def postReply(tid, subject, message):
    """This function posts a reply to the forum.

    Parameters are threadnumber, subject, post.
    The default subject is getResponseData()[1].

    Output is posted (bool), longenough (bool), timeleft.
    posted is True if post succeeded.
    longenough is True if post was over four characters;
    False if too short.
    timeleft is the number of seconds left until the
    user may post again.
    """
    global postkey
    if (postkey == ""):
        return False
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

def getSubs(page):
    """Gets the user's subscribed threads.  Input is
    the page, output is tnums, tnames, new/old, treplies,
    tviews, ttimes, tposters, where t=thread."""
    global postkey
    if (postkey == ""):
        return False
    page = 1
    subSoup = BeautifulSoup(requests.get("https://amblesideonline.org/forum/usercp.php?action=subscriptions&page=" + str(page), cookies = login.cookies).content, "html.parser")
    threads = subSoup.select("table.tborder")[1].select("tr")
    threads.pop(0)
    threads.pop(0)
    threads.pop(-1)
    tnums = []
    tnames = []
    tnoro = []
    treplies = []
    tviews = []
    ttimes = []
    tposters = []
    for thread in threads:
        tnums.append(int(thread.select("td")[2].select("a")[0].get("href")[19:].split('&')[0])) #tid
        tnames.append(thread.select("td")[2].select("a")[-1].get_text()) #name
        tnoro.append(str(thread.select("td")[2].select("a")[-1].get("class"))[11:14]) #new or not
        treplies.append(int(thread.select("td")[3].get_text().replace(',', ''))) #replies
        tviews.append(int(thread.select("td")[4].get_text().replace(',', ''))) #views
        ttimes.append(thread.select("td")[5].select("span")[0].get_text().split('\n')[0]) #last post time
        tposters.append(thread.select("td")[5].select("span")[0].get_text().split('\n')[1][11:]) #last poster
    return tnums, tnames, tnoro, treplies, tviews, ttimes, tposters

def getForum(fid, page):
    """Finds the subitems within a forum.  Returns:
    pages, False, navtitles, navnums, forum numbers, forum names,
    OR
    pages, False, navtitles, navnums, thread numbers,
    thread names, numbers of replies."""
    try:
        login
    except NameError:
        forumSoup = BeautifulSoup(requests.get("https://amblesideonline.org/forum/archive/index.php?forum-" + str(fid) + "-" + str(page) + ".html").content, "html.parser")
    else:
        forumSoup = BeautifulSoup(requests.get("https://amblesideonline.org/forum/archive/index.php?forum-" + str(fid) + "-" + str(page) + ".html", cookies = login.cookies).content, "html.parser")
    if(forumSoup.find_all("div", class_="error") != []):
        return False
    try:
        pages = forumSoup.find("div", class_="multipage").get_text().split(" ")[-2]
    except:
        pages = "1"
    navigation = forumSoup.find_all(class_="navigation")[0]
    navigators = navigation.find_all("a")
    navigators.pop(0)
    navtitles = []
    navnums = []
    for navigator in navigators:
        navtitles.append(navigator.get_text())
        navnums.append(int(navigator.get("href")[58:-5]))
    forumlist = forumSoup.find_all(class_="forumlist")
    if(forumSoup.find_all(class_="forumlist") == []):
        threads = True
    else:
        threads = False
    if(not threads):
        htmls = []
        for item in forumSoup.find_all("li"):
            if(item.find_all("strong") == []):
                htmls.append(item)
        nums = []
        names = []
        for item in htmls:
            soup = BeautifulSoup(str(item), "html.parser")
            a = soup.find("a")
            link = a["href"]
            nums.append(int(link[58:-5]))
            names.append(a.get_text())
        return pages, False, navtitles, navnums, nums, names
    else:
        htmls = []
        for threadlist in forumSoup.find_all("div", class_="threadlist"):
            for thread in threadlist.find_all("li"):
                htmls.append(thread)
        nums = []
        names = []
        replies = []
        for thread in htmls:
            soup = BeautifulSoup(str(thread), "html.parser")
            a = soup.find("a")
            link = a["href"]
            nums.append(int(link[59:-5]))
            names.append(a.get_text())
            try:
                replies.append(int(soup.find("span").get_text().replace(',','')[2:-9]))
            except:
                replies.append(1)
        return pages, False, navtitles, navnums, nums, names, replies
