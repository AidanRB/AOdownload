import aoapi
import getpass
from bs4 import BeautifulSoup

aoapi.username = raw_input("user:")
aoapi.password = getpass.getpass("pass:")
print(aoapi.gatherCredentials())

def getSubfs(forumhtml):
    soup = BeautifulSoup(str(forumhtml), "html.parser")
    htmls = []
    for item in soup.find_all("li"):
        if(item.find_all("strong") == []):
            htmls.append(item)
    nums = []
    for item in htmls:
        soup = BeautifulSoup(str(item))
        a = soup.find("a")
        link = a["href"]
        nums.append(link[58:-5])
    return nums

subnums = getSubfs(str(aoapi.getForum(21,1)[3][0]))

print(aoapi.getForum(subnums[0],1))
