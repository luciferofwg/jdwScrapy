#-*- coding: UTF-8 -*- 
import threading
import time
import dealCurPageHtml
import utils

class myThread (threading.Thread):
	def __init__(self, threadID, workBegin, workEnd):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.workBegin = workBegin
		self.workEnd = workEnd
		
	def run(self):
		utils.logger.info('thread:' + str(self.threadID) +' begin catch ')
		index = int(self.workBegin)
		utils.logger.info('thread:' + str(self.threadID) +'\tindex:' + str(index) + '\tworkBegin:' + str(self.workBegin) + '\tworkEnd:' + str(self.workEnd))
		while index >= int(self.workEnd) and index >= 0:
			url = 'http://jandan.net/ooxx/page-$#comments'
			curUrl = url.replace('$', str(index))
			utils.logger.info('thread:' + str(self.threadID) +'\tcurUrl:' + curUrl)
			if curUrl:
				parentPath = utils.mkdirFolde(utils.getCurPath(), 'Img')
				utils.logger.info('thread:' + str(self.threadID) +'\tparentPath:' + parentPath )
				curPath = utils.mkdirFolde(parentPath, str(index))
				utils.logger.info('thread:' + str(self.threadID) +'\tcurPath:' + curPath )
				jpgPath = utils.mkdirFolde(curPath, 'jpg')
				utils.logger.info('thread:' + str(self.threadID) +'\tjpgPath:' + jpgPath )
				gifPath = utils.mkdirFolde(curPath, 'gif')
				utils.logger.info('thread:' + str(self.threadID) +'\tgifPath:' + gifPath )
				html = utils.getUrlHtml(False,curPath, curUrl)
				if html:
					dealCurPageHtml.praseMianHtml(curPath, self.threadID, html)
				else:
					utils.logger.info('thread:' + str(self.threadID) +'\tgetHtml failed.')
			else:
				utils.logger.info('reload curUrl failed')
			index-=1
		utils.logger.info('thread:' + str(self.threadID) +' complete catch ')
def createThread(threadCount, maxCatchPage, curPage):
	threadIndex = 0
	threads = []
	utils.logger.info('maxCatchPage:' + str(maxCatchPage) + ',curPage:' + str(curPage))
	workBegin = []
	workEnd = []

	if int(maxCatchPage) >= 1 and int(maxCatchPage) <=5:
		#create one size thread
		workBegin.append(int(curPage))
		workEnd.append(int(curPage))

		thread = myThread(threadIndex, workBegin[0], workEnd[0])
		thread.start()

	elif int(maxCatchPage) > int(threadCount):
		#create five size thread,and distribution mession
		#The number of tasks each thread will handle
		avgWork = int(maxCatchPage)//int(threadCount)
		leftWork = int(maxCatchPage)/int(threadCount)

		for i in range(0, threadCount):
			if 0 == i:
				workBegin.append(int(curPage))
				workEnd.append(workBegin[0] -avgWork )
			else:
				if leftWork:
					workBegin.append(workEnd[i-1] - 1)
					workEnd.append(workBegin[i] -avgWork )
				else:
					workBegin.append(workEnd[i-1] - 1)
					workEnd.append(workBegin[i] -avgWork  + leftWork)

		if workBegin and workEnd:
			for i in range(0, len(workBegin)):
				#utils.logger.info('index=' + str(i) + ', workBegin['+str(i)+']='+ str(workBegin[i]) + ',workEnd['+str(i)+']='+str(workEnd[i]))
				thread = myThread(threadIndex, workBegin[i], workEnd[i])
				threadIndex+=1
				thread.start()
				threads.append(thread)

		for t in threads:
			t.join()