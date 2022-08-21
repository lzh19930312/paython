import requests
from bs4 import BeautifulSoup

# headers = {
#     "User-Agent" : "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
# }


def getContent(url):
    res = requests.get(url)
    bs= BeautifulSoup(res.content, 'html.parser')
    div1 = bs.find(class_='location')
    titels = div1.find_all("a")
    bookName = titels[1].text
    content = bs.find(id='content')
    zhangjie  = bs.find("h1")
    nextUrl = bs.find(class_="bottom_setup_3").next['href']
    return bookName,zhangjie.text,content.text,nextUrl