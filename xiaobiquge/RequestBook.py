from HttpUtils  import getContent
from WriteFile import writeContent
import time


domain = "https://www.xiaobiquge.com/"

# domain = "http://xe7tn.oghey08na.yankun.shop/"

def requestBook(url):
    while True:
        bookName,zhangjie,content,nextUrl = getContent(domain + url)
        writeContent(bookName,zhangjie,content,nextUrl)
        if nextUrl.find('index.html') > -1:
            break
        else:
            url = nextUrl
            time.sleep(1)
