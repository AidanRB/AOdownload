from aoapi import inputLogin, gatherCredentials, getPage
from progress.bar import Bar

logged = False
while(not logged):
    inputLogin()
    logged = gatherCredentials()
print("Success.\n")

threadnum = input("Thread number: ")
firstpage = input("First page:    ")
lastpage  = input("Last page:     ")

progressbar = Bar('Downloading %(index)d/%(max)d', max = lastpage - firstpage + 1, suffix = '%(eta_td)s')

filename = "thread" + str(threadnum) + "pages" + str(firstpage) + "-" + str(lastpage) + ".html"
outfile = open(filename, "w")

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
pageauthors, pagetimes, pageposts, title, pages, navtitles, navnums = getPage(threadnum, firstpage)
outfile.write("<h1 class=\"threadname\">" + title + "</h1>\n<h4 class=\"pages\">Pages " + str(firstpage) + "-" + str(lastpage) + "<h4>\n")

for currentnum in range(lastpage - firstpage + 1):
    pageauthors, pagetimes, pageposts, title, pages, navtitles, navnums = getPage(threadnum, currentnum + firstpage)
    outfile.write("<h2 class=\"page\">Page " + str(currentnum + firstpage) + "</h2>\n\n</div> </div><hr class=\"postdivider\">\n\n")
    for post in zip(pageauthors, pageposts):
        outfile.write("<div class=\"postcontainer\"> <h3 class=\"author\">" +
            post[0] + "</h3> <br> <div class=\"post\">\n" +
            post[1] + "\n</div> </div> <br/> <hr class=\"postdivider\">\n\n")
    progressbar.next()

outfile.write("</body>\n</html>\n")
outfile.close()
progressbar.finish()
print("Downloaded to " + filename)
