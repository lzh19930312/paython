from RequestBook import requestBook
import threading


urls = ['/236/236069/133208643.html','/10/10417/119803763.html','/12/12149/135263561.html']


for url in urls:
    book = threading.Thread(name=url, target=requestBook, args=(url,))
    book.start()