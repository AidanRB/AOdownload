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

outfile.write("<html><head><style>\nhtml {\n    background: #212121;\n    color: white;\n    font-family: noto sans cjk jp, roboto, open sans, sans;\n}\n\n.threadname {\n    letter-spacing: 3px;\n    font-weight: lighter;\n    font-size: 250%;\n    text-align: center;\n}\n\n.pages {\n    font-size: 75%;\n    text-align: center;\n    transform: scale(1, 0.9);\n    font-style: italic;\n    font-weight: bold;\n}\n\n.postcontainer {\n    margin: 10px;\n    margin-bottom: 75px;\n    margin-top: 150px;\n    font-weight: normal;\n}\n\n.postcontainer:first-of-type {\n    margin-top: 75px;\n}\n\n.postdivider {\n    position: absolute;\n    content: \"\";\n    background: white;\n    height: 1px;\n    display: block;\n    left: 50%;\n    width: 200px;\n    margin-left: -100px;\n    border: 0;\n}\n\n.author {\n    padding: 10px;\n    margin-bottom: 0px;\n    width: fit-content;\n    font-size: 200%;\n}\n\n.post {\n    margin-top: 10px;\n    padding: 10px;\n    font-size: 100%;\n}\n</style></head>\n<body>\n")
pageauthors, pagetimes, pageposts, title, pages, navtitles, navnums = getPage(threadnum, firstpage)
outfile.write("<h1 class=\"threadname\">" + title + "</h1><br>\n<h4 class=\"pages\">Pages " + str(firstpage) + "-" + str(lastpage) + "<h4><br><br>\n\n")

for currentnum in range(lastpage - firstpage + 1):
    pageauthors, pagetimes, pageposts, title, pages, navtitles, navnums = getPage(threadnum, currentnum + firstpage)
    outfile.write("<h2 class=\"page\">Page " + str(currentnum + firstpage) + "</h2><br>\n\n")
    for post in zip(pageauthors, pageposts):
        outfile.write("<div class=\"postcontainer\"><h3 class=\"author\">" + post[0] + "</h3><br><div class=\"post\">\n" + post[1].replace("\n", "<br>\n") + "\n</div></div><br><br><br><hr class=\"postdivider\">\n\n")
    progressbar.next()
        
outfile.write("</body>\n</html>\n")
outfile.close()
progressbar.finish()
print("Downloaded to " + filename)
