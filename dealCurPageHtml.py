#-*- coding: UTF-8 -*- 
import utils
import os
import os.path
import re

def praseMianHtml(path, threadId, data):
	utils.logger.debug('threadId:' + 'parseHtml begin.')

	jpgReg = re.compile(r'<a href="//(.*?).jpg')
	gifReg = re.compile(r'<a href="//(.*?).gif')

	urlJpgs = re.findall(jpgReg, data)
	if urlJpgs:
		index = 1
		for url in  urlJpgs:
			newUrl = 'http://' + url + '.jpg'
			utils.logger.debug('threadId:' + str(threadId) + ' download url:'+newUrl)
			newPath = path + '\\' + 'jpg'
			utils.downLoadIng(newPath, index, newUrl)
			utils.logger.debug('threadId:' + str(threadId) + ' download url:'+newUrl + ' Complete')
			index+=1
	else:
		utils.logger.info('praseMianHtml get jpg url failed.')

	urlGifs = re.findall(gifReg, data)
	if urlGifs:
		index = 1
		for url in  urlGifs:
			newUrl = 'http://' + url + '.gif'
			utils.logger.debug('threadId:' + str(threadId) + ' download url:'+newUrl)
			newPath = path + '\\' + 'gif'
			utils.downLoadIng(newPath, index, newUrl)
			utils.logger.debug('threadId:' + str(threadId) + ' download url:'+newUrl + ' Complete')
			index+=1
	else:
		utils.logger.info('threadId:' + str(threadId) + ' praseMianHtml get gif url failed.')