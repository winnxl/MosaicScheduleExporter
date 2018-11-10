#-*- coding: utf-8 -*-
import scrapy, csv
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
											# download scrapy library

class MosaicSpider(scrapy.Spider):
	name = "mosaic"

	outfile = open("output.csv", "w", newline="")
	writer = csv.writer(outfile)


	def start_requests(self):
		urls = [
			#'file:///C:/workspace/My%20Class%20Schedule.html',		# local (urls are absolute paths only)
			'http://c.nicolak.ca/3XA3/My%20Class%20Schedule.html',	# web	(for testing)
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):	
		course = "win0divDERIVED_REGFRM1_DESCR20$"
		comp = "MTG_COMP$"
		sched = "MTG_SCHED$"
		loc = "MTG_LOC$"

		count = 0
		row = 0

		for i in response.css('td.PAGROUPDIVIDER'):
			courseNo = course + str(count)
			count = count + 1 				# will need to be moved with check
			
			for j in range(0, 2): 			# range need to be changed to 3 once check is implemented (lecture, tutorial, lab)
											# implement check for component.value = 'Lecture', then count + 1.
				compNo = comp + str(row)
				schedNo = sched + str(row)
				locNo = loc + str(row)				
				row = row + 1 				# will need to be moved with check
	
				courseName = i.xpath('//*[@id=$val]/table/tbody/tr[1]/td/text()', val= courseNo).extract()
				component = i.xpath('//*[@id=$val]/text()', val= compNo).extract()
				schedule = i.xpath('//*[@id=$val]/text()', val= schedNo).extract()
				location = i.xpath('//*[@id=$val]/text()', val= locNo).extract()					
			
				self.writer.writerow([courseName, component, schedule, location])

				yield {	
					'course': courseName,
					'component': component,
					'schedule': schedule,
					'location': location,							
				}

	def close(self):
		self.outfile.close()
		print("-----Check to see if this is closed-----")

process = CrawlerProcess({
	'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(MosaicSpider)
process.start() 							# script will block here until the crawling is finished


'''
Sample Output:

['ECON 1BB3 - Introductory Macroeconomics'],['Lecture'],['We 2:30PM - 3:20PM'],['MDCL 1305']
['ECON 1BB3 - Introductory Macroeconomics'],['Tutorial'],['Fr 12:30PM - 1:20PM'],['ABB 271']
['SFWRENG 2FA3 - Discrete Math. Application II'],['Lecture'],['TuThFr 11:30AM - 12:20PM'],['ITB 137']
['SFWRENG 2FA3 - Discrete Math. Application II'],['Tutorial'],['Mo 11:30AM - 12:20PM'],['BSB 108']
['SFWRENG 3A04 - Software Design III'],['Lecture'],['TuWeFr 3:30PM - 4:20PM'],['HH 109']
['SFWRENG 3A04 - Software Design III'],['Tutorial'],['Mo 3:30PM - 5:20PM'],['ABB 164']
['SFWRENG 3S03 - Software Testing'],['Lecture'],['MoWeTh 1:30PM - 2:20PM'],['CNH B107']
['SFWRENG 3S03 - Software Testing'],['Tutorial'],['Tu 4:30PM - 5:20PM'],['ETB 235']
['SFWRENG 4C03 - Comp Networks & Security'],['Lecture'],['MoWeTh 5:30PM - 6:20PM'],['JHE 264']
['SFWRENG 4C03 - Comp Networks & Security'],['Laboratory'],['Fr 8:30AM - 11:20AM'],['ITB 236']

Schedule needs to be sliced every 2 characters until space where time follows.
Q: Can also be be sliced by proper case?

'''