## @file parseMosaic.py
#  @author Cassandra Nicolak, Winnie Liang, Michelle Lueng
#  @brief macID: nicolace, x, x
## @date 11/8/2018

## @brief Imported packages and libraries. 
#  @details Imports the scrapy and subprocess libraries.
import subprocess as sp
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

# State Variables
dataList = list()						# datalist to be passed


## @brief A spider class that Scrapy uses to scrape information from a website. This class must also subclass scrapy.Spider.
class MosaicSpider(scrapy.Spider):
	name = "mosaic"

    ## @brief A method that will be called to handle the response downloaded for each of the requests made. 
    #  @details The method parses the response, extracting the scraped data as dicts.
    #  @param response an instance of TextResponse that holds the page content and has further helpful methods to handle it.
	def parse(self, response):	

		# selector variables
		course = "win0divDERIVED_REGFRM1_DESCR20$"
		courseStatus = "STATUS$"
		comp = "MTG_COMP$"
		sched = "MTG_SCHED$"
		loc = "MTG_LOC$"
		dateRange = "MTG_DATES$"

		# initialization for counts
		count = 0
		row = 0

		# loops through header rows
		for i in response.css('td.PAGROUPDIVIDER'):

			# initialization
			courseNo = course + str(count)
			statusNo = courseStatus + str(count)
			firstLecFound = False			# flag for when to break loop and iterate header/course
			repeatComponent = ''

			count = count + 1 				# count for headers

			# use xpath selector for status check
			status = i.xpath('//*[@id=$val]/text()', val= statusNo).extract()[0]
			
			# only parse courses that have an 'Enrolled' status.


			# loops through content rows
			for j in range(0, 10):			#todo: this value may need to be set to 35

				# val
				compNo = comp + str(row)
				schedNo = sched + str(row)
				locNo = loc + str(row)
				dateRangeNo = dateRange + str(row)

				# use xpath selectors	
				courseName = i.xpath('//*[@id=$val]/table/tbody/tr[1]/td/text()', val= courseNo).extract()[0]
				component = i.xpath('//*[@id=$val]/text()', val= compNo).extract()[0]
				schedule = i.xpath('//*[@id=$val]/text()', val= schedNo).extract()[0]
				location = i.xpath('//*[@id=$val]/text()', val= locNo).extract()[0]
				dates = i.xpath('//*[@id=$val]/text()', val= dateRangeNo).extract()[0]

				# conditionals				
				if str(component) == str("Lecture"):		# check if lecture
					if not firstLecFound:				# if it's the first lecture, set flag and continue
						firstLecFound = True
					else:
						break							# if it's the second time a lecture is found, break the inner loop

				if str(component) != str("\xa0"):		# account for multiple rows for a component
					repeatComponent = component
				else:
					component = repeatComponent
				
				if str(status) == str("Enrolled"):
					# adds to data list
					dataList.append((courseName, component, schedule, location, dates))
				
				row = row + 1 							# count for content rows


# allows for executing scrapy spiders outside of the scrapy shell.
process = CrawlerProcess({
	'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})


## @brief A def that allows other modules to start the crawling process.
#  @details Allows other modules to start the crawling process.
#  @param passed_url a single url to be added to the start_url list that contains only one item.
#  @return Returns a copy of the global list, dataList. This contains the parsed data.
def runMe(passed_url):							# accepts the URL to parse
	sp.call('cls',shell=True)					# clears console

	process.crawl(MosaicSpider, start_urls = [passed_url])

	process.start() 							# script will block here until the crawling is finished
	return dataList.copy()						# returns the data list

