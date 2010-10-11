import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor, BaseSgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import XPathItemLoader
from giscrape.items import *
from scrapy.item import Item, Field
from scrapy import log
from giscrape.orm import *

log.start()

class customExtractor(SgmlLinkExtractor):
  def extract_links(self, response):
    response.body = response.body.replace('\\','')
    return SgmlLinkExtractor.extract_links(self,response)
    
class TcadSpider(CrawlSpider):
  name = 'tcad'
  allowed_domains = ['http://www.traviscad.org/']

  start_urls = []
  
  rules = (
    Rule( customExtractor(),callback='parse_tcad' ),
  )
  
  def parse_tcad(self, response):
    parcel = XPathItemLoader(item=TCADParcelItem(), response=response)

    parcel.add_value('url', response.url)
    parcel.add_xpath('parcel_id','//font[text()="Property ID Number:"]/../../td[2]/font/b/text()')
    parcel.add_xpath('owner','//td[text()="Owner\'s Name"]/../td[@class="reports_blacktxt"]/font/b/text()')
    parcel.add_xpath('owner_address','//td[text()="Owner\'s Name"]/../../tr[1]/td[@class="reports_blacktxt"]/font/b/text()')
    parcel.add_xpath('address','//td[text()="Owner\'s Name"]/../../tr[2]/td[@class="reports_blacktxt"]/font/b/text()')

    parcel.add_xpath('land_value','//font[text()="Land Value"]/../../td[@class="reports_blacktxt"]/p/text()')
    parcel.add_xpath('improvement_value','//font[text()="Improvement Value"]/../../td[@class="reports_blacktxt"]/p/text()')
    parcel.add_xpath('total_value','//font[text()="Total Value"]/../../td[@class="reports_blacktxt"]/p/text()') 
    
    parcel.add_xpath('land_acres','//font[text()="Land Acres"]/../../td[@class="reports_blacktxt"]/p/text()')   
    parcel.add_xpath('neighborhood','//font[text()="Neighborhood Code"]/../../td[@class="reports_blacktxt"]/p/text()')
    
    hxs = HtmlXPathSelector(response)
    for improvement in hxs.select('').extract():
      i = XpathItemLoader(item=TCADImprovementItem(), response=improvement)
   
    for segment in hxs.select('').extract():
      s = XpathItemLoader(item=TCADSegmentItem(), response=improvement)   
    
    for history in hxs.select('').extract():
      h = XpathItemLoader(item=TCADValueHistoryItem(), response=improvement)
    
    return l.load_item()