#-*- coding: UTF-8 -*- 
import logging
import os
import os.path
import shutil

FORMATTER = '%(asctime)-4s [%(name)s] %(filename)-20s [line:%(lineno)03d]: %(levelname)-8s %(message)s'
format_dict = {
   1 : logging.Formatter(FORMATTER),
   2 : logging.Formatter(FORMATTER),
   3 : logging.Formatter(FORMATTER),
   4 : logging.Formatter(FORMATTER),
   5 : logging.Formatter(FORMATTER)
}

class Logger():
	def __init__(self, logname, loglevel, logger):
		# 创建一个logger
		self.logger = logging.getLogger(logger)
		self.logger.setLevel(logging.DEBUG)

		# 创建一个handler，用于写入日志文件
		fh = logging.FileHandler(logname)
		fh.setLevel(logging.DEBUG)

		# 再创建一个handler，用于输出到控制台
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		# 定义handler的输出格式
		formatter = format_dict[int(loglevel)]
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)

		# 给logger添加handler
		self.logger.addHandler(fh)
		self.logger.addHandler(ch)

	
	def getlog(self):
		return self.logger
