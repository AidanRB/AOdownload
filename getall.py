import aoapi
import getpass
from bs4 import BeautifulSoup

aoapi.username = raw_input("user:")
aoapi.password = getpass.getpass("pass:")
aoapi.gatherCredentials()

# This finds all threads within a given forum
# to be passed to the downloader individually
rootforum = 14
baseforums = []
currentforum = aoapi.getForum(rootforum, 1)
if(not currentforum[1]):
    for page in range(int(currentforum[0])):
        baseforums += aoapi.getForum(rootforum, page)[4]
else:
    baseforums = [rootforum]

