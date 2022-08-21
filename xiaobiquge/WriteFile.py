from LogUtils import logger

def writeContent(bookName, zhangjie, context, path):
    book  = open("./txt/{}.txt".format(bookName), mode="a+", encoding="utf-8")
    book.write(zhangjie + "\n")
    book.write(context + "\n")
    logger.info("写入{} {} 完成, url {}".format(bookName, zhangjie, path))