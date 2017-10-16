import aoapi, re, requests
from bs4 import BeautifulSoup, SoupStrainer

pagglink = re.compile('.*photos\.app\.goo\.gl.*')
pgclink = re.compile('.*photos\.google\.com/share.*')

authed = False
while(not authed):
    aoapi.inputLogin()
    authed = aoapi.gatherCredentials()

print("auth\n")

tofixlinks = []
pfixedlinks = []
lastpage = aoapi.getPage(2780, 1)[4]
pages = aoapi.getPages(2780, int(lastpage) - 5, int(lastpage))
print("got " + str(int(lastpage) - 5) + "-" + str(int(lastpage)) + "\n")
for post in pages[2]:
    for link in BeautifulSoup(post, 'html.parser',  parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            if pagglink.match(link['href']):
                tofixlinks.append(link['href'])
                print("pagg " + link['href'] + "\n")
            if pgclink.match(link['href']):
                pfixedlinks.append(link['href'])
                print("pgc " + link['href'] + "\n")
                
fixedlinks = []
for link in tofixlinks:
    page = requests.get(link)
    fixedlinks.append(page.url)
    print("resolved " + link + "\nto " + page.url + "\n")

pfixedends = []
for link in pfixedlinks:
    pfixedends.append(link[-100:])

topost = '[b]Links:[/b]\n\n'
for link in fixedlinks:
    if not link[-100:] in pfixedends:
        topost += link + '\n\n'

aoapi.postReply(2780, "Unshortened links", topost)
print("\n\n\n" + topost)


