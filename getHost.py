#-*- coding: UTF-8 -*- 
import os
import utils
import re
			
def getCurPage(data):
	divReg = re.compile(r'<div class="cp-pagenavi">(.*?)</div>', re.S)
	spanReg =re.compile(r'<span class="current-comment-page">(.*?)</span>', re.S)
	rmvReg =re.compile(r']|\[', re.S)
	
	results = re.search(divReg, data)
	results = re.search(spanReg, results.group(1))
	page = re.sub(rmvReg, '', results.group(1))
	if page:
		return page
	else:
		return None

def getMainUrl(url):
	utils.logger.info('url:' + url )
	data = utils.getUrlHtml(False, '', url)
	if data:
		return getCurPage(data)
	else:
		utils.logger.debug('getMainUrl getHtml failed,url:' + url)
		return None