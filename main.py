#-*- coding: UTF-8 -*- 
import getHost
import myThread
import utils
import time

def main():
	url = 'http://jandan.net/ooxx'
	curPage = getHost.getMainUrl(url)
	utils.logger.info('please input nums you want catch (0~' + curPage + ') :')
	maxCatchPage = int(raw_input(""))
	while maxCatchPage>int(curPage) or maxCatchPage<0:
		utils.logger.info('please input nums you want catch (0~' + curPage + ') :')
		maxCatchPage = int(raw_input(""))

	utils.logger.info('please 10input thread nums you want lanuch (n*5&less20):')
	threadCount = int(raw_input(""))
	while threadCount>20 or threadCount<0:
		utils.logger.info('please input thread nums you want lanuch (n*5&less20):')
		threadCount = int(raw_input(""))

	start = time.clock()
	if curPage:
		myThread.createThread(threadCount, maxCatchPage, curPage)
		utils.zip('Img')
	else:
		print 'main() get tilUrls failed.'
	end = time.clock()
	utils.logger.info("process used time: %f s" % (end - start))
if __name__ == "__main__":
	main()
else:
	print "called from intern."