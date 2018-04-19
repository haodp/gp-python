#-*- coding:utf-8 -*-
import logging
import os,sys

logger = logging.getLogger('gupiaoTool')
logger.setLevel(logging.INFO)

# dir = os.path.split(os.path.realpath(__file__))[0]
dir = os.path.dirname(sys.executable)
print(dir)
# 创建一个handler,用于写入日志文件
fn = logging.FileHandler(dir + '/gupiaoTool.log', 'a')
# 定义handler的输出格式formatter
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
formatter = logging.Formatter(fmt, datefmt)
fn.setFormatter(formatter)
logger.addHandler(fn)
