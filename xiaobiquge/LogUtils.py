
import logging
import time


class logFrame:
   def getlogger(self):
       self.logger = logging.getLogger("logger")
       # 判断是否有处理器，避免重复执行
       if not self.logger.handlers:
           # 日志输出的默认级别为warning及以上级别，设置输出info级别
           self.logger.setLevel(logging.DEBUG)
           # 创建一个处理器handler  StreamHandler()控制台实现日志输出
           sh = logging.StreamHandler()
           # 创建一个格式器formatter  （日志内容：当前时间，文件，日志级别，日志描述信息）
           formatter = logging.Formatter(fmt="当前时间是%(asctime)s,文件是%(filename)s,行号是%(lineno)d，日志级别是%(levelname)s，"
                                          "描述信息是%(message)s",datefmt="%Y/%m/%d %H:%M:%S")

           # 创建一个文件处理器，文件写入日志
           fh = logging.FileHandler(filename="./log/{}_log.txt".format(time.strftime("%Y_%m_%d %H",time.localtime())),
                                    encoding="utf8")
           # 创建一个文件格式器f_formatter
           f_formatter = logging.Formatter(fmt="%(asctime)s,文件%(filename)s,行号%(lineno)d，日志级别 %(levelname)s， "
                                               "%(message)s",datefmt="%Y/%m/%d %H:%M:%S")

           # 关联控制台日志器—处理器—格式器
           self.logger.addHandler(sh)
           sh.setFormatter(formatter)
           # 设置处理器输出级别
           sh.setLevel(logging.ERROR)

           # 关联文件日志器-处理器-格式器
           self.logger.addHandler(fh)
           fh.setFormatter(f_formatter)
           # 设置处理器输出级别
           fh.setLevel(logging.DEBUG)

       return self.logger
log = logFrame()
logger = log.getlogger()

if __name__ == '__main__':
    # 输出日志
    try:
        b = int(input("请输入一个除数:"))
        num = 4/b
        logger.info(f"4/{b}={num},计算完成")
        logger.debug("这条对了")
    except Exception as error:
        print(str(error))
        logger.error(str(error))