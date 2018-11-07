#-*- coding: utf-8 -*-
import subprocess as sp

# uses scrapy library
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

# GLOBAL VARIABLES
dataList = list()						# datalist to be passed

# MAIN CLASS
class MosaicSpider(scrapy.Spider):
	name = "mosaic"


	def parse(self, response):	

		# selector variables
		course = "win0divDERIVED_REGFRM1_DESCR20$"
		comp = "MTG_COMP$"
		sched = "MTG_SCHED$"
		loc = "MTG_LOC$"

		# initialization for counts
		count = 0
		row = 0

		# loops through header rows
		for i in response.css('td.PAGROUPDIVIDER'):

			# initialization
			courseNo = course + str(count)
			firstLecFound = False			# flag for when to break loop and iterate header/course
			repeatComponent = ''

			count = count + 1 				# count for headers

			# loops through content rows
			for j in range(0, 5):

				# val
				compNo = comp + str(row)
				schedNo = sched + str(row)
				locNo = loc + str(row)				

				# use xpath selectors	
				courseName = i.xpath('//*[@id=$val]/table/tbody/tr[1]/td/text()', val= courseNo).extract()
				component = i.xpath('//*[@id=$val]/text()', val= compNo).extract()
				schedule = i.xpath('//*[@id=$val]/text()', val= schedNo).extract()
				location = i.xpath('//*[@id=$val]/text()', val= locNo).extract()	


				# conditionals				
				if str(component) == "['Lecture']":		# check if lecture
					if not firstLecFound:				# if it's the first lecture, set flag and continue
						firstLecFound = True
					else:
						break							# if it's the second time a lecture is found, break the inner loop

				if str(component) != "['\\xa0']":		# account for multiple rows for a component
					repeatComponent = component
				else:
					component = repeatComponent

				if len(str(component)) < 3:				# breaks if no value is returned
					break					


				# adds to data list
				dataList.append((courseName, component, schedule, location))
				
				row = row + 1 							# count for content rows

				#yield {	
				#	'course': courseName,
				#	'component': component,
				#	'schedule': schedule,
				#	'location': location,							
				#}

	def close(self):
		self.outfile.close()
		print("-----Check to see if this is closed-----")

process = CrawlerProcess({
	'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})


# called from runParse.py
def runMe(passed_url):							# accepts the URL to parse
	sp.call('cls',shell=True)					# clears console

	process.crawl(MosaicSpider, start_urls = [passed_url])

	process.start() 							# script will block here until the crawling is finished
	return dataList.copy()						# returns the data list

