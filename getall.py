import aoapi
import getpass
import os
from bs4 import BeautifulSoup
from progress.bar import Bar

verbose = False
foldername = "what_have_I_done"

logged = False
while(not logged):
    aoapi.inputLogin()
    logged = aoapi.gatherCredentials()
print("Success.\n")

if not os.path.exists(foldername):
    os.makedirs(foldername)

print("Beginning forum listing download")

rootforum = 14
forums = []
currentforum = aoapi.getForum(rootforum, 1)
if(not currentforum[1]):
    for page in range(int(currentforum[0])):
        forums += aoapi.getForum(rootforum, page)[4]
else:
    forums = [rootforum]

print("Forum listing downloaded")
if(verbose):
    print(forums)
print("\nBeginning thread listing download")

threads = []
for fnumber in forums:
    page1 = aoapi.getForum(fnumber, 1)
    threads += page1[4]
    print("Added forum " + str(fnumber) + " page 1")
    if(verbose):
        print(page1[4])
    if(page1[0] != 1):
        for page in range(int(page1[0]) - 1):
            threadstoadd = aoapi.getForum(fnumber, page + 2)[4]
            threads += threadstoadd
            print("Added forum " + str(fnumber) + " page " + str(page + 2))
            if(verbose):
                print(threadstoadd)
    print

threads = sorted(threads)

print("Thread listing downloaded")
if(verbose):
    print(threads)
print("\nBeginning threads download")

firstpage = 1
for i in range(len(threads)):
    threadnum = threads[i]
    lastpage = int(aoapi.getPage(threadnum, 1)[4])

    filename = foldername + "/thread" + str(threadnum) + "pages" + str(firstpage) + "-" + str(lastpage) + ".html"
    outfile = open(filename, "w")

    print("Downloading thread " + str(threadnum) + " (" + str(i) + "/" + str(len(threads)) + ") to page " + str(lastpage) + " to " + filename)

    progressbar = Bar('Downloading %(index)d/%(max)d', max = lastpage - firstpage + 1, suffix = '%(eta_td)s')

    outfile.write("""<html> <head> <style>
        html {
            background: bgcolor;
            color: fgcolor;
            font-family: noto sans cjk jp, roboto, open sans, sans;
        }

        .threadname {
            letter-spacing: 3px;
            font-weight: lighter;
            font-size: 250%;
            text-align: center;
        }

        .pages {
            font-size: 75%;
            text-align: center;
            transform: scale(1, 0.9);
            font-style: italic;
            font-weight: bold;
        }

        .postcontainer {
            margin: 10px;
            margin-bottom: 0px;
            margin-top: 20px;
            font-weight: normal;
        }

        .postcontainer:first-of-type {
            margin-top: 10px;
        }

        .postdivider {
            position: absolute;
            content: "";
            background: fgcolor;
            height: 1px;
            display: block;
            left: 50%;
            width: 200px;
            margin-left: -100px;
            border: 0;
        }

        .author {
            padding: 10px;
            margin-bottom: 0px;
            width: fit-content;
            font-size: 200%;
        }

        .post {
            margin-top: 10px;
            padding: 10px;
            font-size: 100%;
        }

        .page {
            padding-top: 20px;
            font-size: 75%;
            text-align: center;
            transform: scale(1, 0.9);
            font-style: italic;
            font-weight: bold;
        }
        </style> </head>
        <body>
        """.replace("bgcolor", "white").replace("fgcolor", "black"))
    for trynumber in range(100):
        try:
            pageauthors, pagetimes, pageposts, title, pages, navtitles, navnums = aoapi.getPage(threadnum, firstpage)
            break
        except:
            pass
    outfile.write("<h1 class=\"threadname\">" + title + "</h1>\n<h2 class=\"pages\">Pages " + str(firstpage) + "-" + str(lastpage) + "<h2>\n")

    for currentnum in range(lastpage - firstpage + 1):
        for trynumber in range(100):
            try:
                pageauthors, pagetimes, pageposts, title, pages, navtitles, navnums = aoapi.getPage(threadnum, currentnum + firstpage)
                break
            except:
                pass
        outfile.write("<h2 class=\"page\">Page " + str(currentnum + firstpage) + "</h2>\n\n</div> </div><hr class=\"postdivider\">\n\n")
        for post in zip(pageauthors, pageposts):
            outfile.write("<h1 class=\"author\">" + post[0] + "</h1> <div class=\"post\">\n" + post[1] + "\n</div>\n\n")
        progressbar.next()

    outfile.write("</body>\n</html>\n")
    outfile.close()
    progressbar.finish()
