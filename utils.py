#-*- coding: UTF-8 -*- 
import urllib
import urllib2
import os
import os.path
import shutil
from random import Random
import zipfile
import sys,time
import gzip
import log

#获取当前文件绝对路径
def getCurPath():
	return os.getcwd()

FILENAME = getCurPath() + '\\' + 'log.log'
LOG_LINE = '-----------------------------------------------------------'
#初始化日志模块
logger = log.Logger(FILENAME, 1, "root").getlog()

#测试打印
def printTable(Tab):
	for it in Tab:
		print it

#读取数据
def readData(filePath, mode):
	fo = open(filePath, mode)
	try:
		data = fo.read()
	finally:
		fo.close()
	return data

#存储文本
def writeData(filePath, data, mode):
	logger.info('filePath:' + filePath )
	fo = open(filePath, mode)
	try:
		fo.write(data)
		fo.close()
	finally:
		fo.close()
		
#随机生成字符串
def getRandomName(randomlength=12):
	str = ''
	chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
	length = len(chars) - 1
	random = Random()
	for i in range(randomlength):
		str+=chars[random.randint(0, length)]
	return str

#创建文件夹
def mkdirFolde(path, foldeName):
	pathEx = path + '\\' + foldeName
	isExist = os.path.exists(pathEx)
	if not isExist:
		logger.info('Folde #' + foldeName + '# create success')
		os.makedirs(pathEx)

	return pathEx

#清除之前文件和文件件
def clearFiles(top):
	for root, dirs, files in os.walk(top, topdown=False):
		for name in files:
			if -1 == name.find(".py", 0) and -1 == name.find(".jpg", 0) and -1 == name.find(".pyc", 0):
				os.remove(os.path.join(root, name))				
		for name in dirs:
			if -1 !=name.find("dat"):
				os.rmdir(os.path.join(root, name))
	
#进度条显示
def showBarBegin():
	myLog.write('i', '\rProcess [0%%] |#')
def showBarBegin(num=1, sum=100, bar_word="#"):
	time.sleep(0.1)
	rate = float(num) / float(sum)
	rate_num = int(rate * 100)
	print '\rProcess [%d%%] |' %(rate_num),
	for i in range(0, num):
		os.write(1, bar_word)
	sys.stdout.flush()
def showBarEnd():
	os.write(1, '|')
	sys.stdout.flush()

def unZipData(curPath, data):
	if curPath != '':
		fileName = curPath + '\\' + 'temp.dat'
	else:
		fileName = os.getcwd() + '\\' + 'temp.dat'
		
	logger.info('unZipData curPath is:' + curPath)
	logger.info('unZipData fileName is:' + fileName)
	writeData(fileName, data, 'wb')
	f = gzip.open(fileName, 'rb')
	html = f.read()
	f.close()
	#删除临时文件
	os.remove(fileName)
	return html
		
#直接获取url的html
def getUrlHtml(isZipPack, curPath, url):
	try:
		logger.info('get page url is :' + url )
		req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
							'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
							'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
							'Accept-Encoding':'gzip, deflate',
					  		'Accept-Language':'zh-CN,zh;q=0.8',
							'Connection':' keep-alive',
							'Referer':'http://www.txt53.com/' #注意如果依然不能抓取的话，这里可以设置抓取网站的host
						}
		req_timeout = 15#默认时间10s
		req = urllib2.Request(url, None, req_header)
		fp = urllib2.urlopen(req, None, req_timeout)
		data = fp.read()
		if isZipPack == False:
			html = unZipData(curPath, data)
			return html
		else:
			return data

	#except urllib2.URLError, e:
	#	if hasattr(e,"reason"):
	#		logger.info('get host page failed,error:' + e.reason )
	#	return None

	except IOError, error:
		logger.info("getUrlHtml download error: %s error %s" % (url, error))
		return None
	except Exception, e:
		logger.info("getUrlHtml Exception :" + str(e))
		return None


def downLoadIng(path, index, url):
	try:
		urlopen=urllib.URLopener()
		#伪装浏览器
		req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
						'Accept':'text/html;q=0.9,*/*;q=0.8',
						'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
						'Accept-Encoding':'gzip',
						'Connection':'close',
						'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
					}
		req_timeout = 10#默认时间10s
		req = urllib2.Request(url, None, req_header)
		fp = urllib2.urlopen(req, None, req_timeout)
		data = fp.read()
		fp.close()
		if -1 != url.find('.jpg'):
			fileName = path + '\\' + str(index) + ".jpg"
		elif -1 != url.find('.gif'):
			fileName = path + '\\' + str(index) + ".gif"
		file = open(fileName, "w+b")
		file.write(data)
		file.close()
	except IOError, error:
		logger.info("downLoadIng download error: %s\nerror %s" % (url, error))
	except Exception, e:
		logger.info("downLoadIng Exception :" + str(e))


def zip(srcFilPath):
	logger.info("zip srcFilPath :" + srcFilPath)
	z = zipfile.ZipFile(srcFilPath + '.zip', 'w', zipfile.ZIP_DEFLATED)
	for dirpath, dirnames, filenames in os.walk(srcFilPath):
		for filename in filenames:
			z.write(os.path.join(dirpath, filename))
	z.close()
