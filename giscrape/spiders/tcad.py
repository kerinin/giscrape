import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor, BaseSgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import XPathItemLoader
from giscrape.items import *

from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from scrapy import *
from giscrape.orm import *
from geoalchemy import *


log.start()

class customExtractor(SgmlLinkExtractor):
  def extract_links(self, response):
    response.body = response.body.replace('\\','')
    return SgmlLinkExtractor.extract_links(self,response)
    
class TcadSpider(BaseSpider):
  name = 'tcad'
  allowed_domains = ['http://www.traviscad.org/']

  session = Session()
  shady = WKTSpatialElement("POINT(%s %s)" % (-97.699009500000003, 30.250421899999999) )
  
  start_urls = ['http://www.traviscad.org/travisdetail.php?theKey=%s&show_history=Y' % x[0] for x in session.query(TCAD_2010.prop_id).filter(TCAD_2010.market_value == None).filter(TCAD_2010.prop_id > 0).order_by(TCAD_2010.the_geom.centroid().distance(shady.transform(2277)))[:30000] ]
  
  def parse(self, response):
    response.body = response.body.replace('\\','').replace('\xa0','')
    parcel = XPathItemLoader(item=TCADParcelItem(), response=response)

    parcel.add_value('url', response.url)
    parcel.add_xpath('prop_id','//font[text()="Property ID Number:"]/../../td[3]/font/b/text()')
    parcel.add_xpath('owner','//td[text()="Owner\'s Name"]/../td[@class="reports_blacktxt"]/font/b/text()')
    parcel.add_xpath('owner_address','//td[text()="Owner\'s Name"]/../../tr[2]/td[2]/text()')
    parcel.add_xpath('address','//td[text()="Owner\'s Name"]/../../tr[3]/td[2]/text()')

    parcel.add_xpath('land_value','//font[text()="Land Value"]/../../td[@class="reports_blacktxt"]/p/text()')
    parcel.add_xpath('improvement_value','//font[text()="Improvement Value"]/../../td[@class="reports_blacktxt"]/p/text()')
    parcel.add_xpath('market_value','//font[text()="Total Value"]/../../td[@class="reports_blacktxt"]/p/text()') 
    
    parcel.add_xpath('acreage','//font[text()="Land Acres"]/../../td[@class="reports_blacktxt"]/p/text()')   
    parcel.add_xpath('neighborhood','//font[text()="Neighborhood Code"]/../../td[@class="reports_blacktxt"]/text()')
    
    parcel.add_xpath('improvement_area', '//font[text()="Total Living Area"]/../../td[2]//b/text()')
    
    def improvement(text, url):
      response = http.TextResponse(url=url, body=str(text))
      i = XPathItemLoader(item=TCADImprovementItem(), response=response)
      
      i.add_xpath('id', '//td[1]/text()')
      i.add_xpath('state_category', '//td[2]/text()')
      i.add_xpath('description', '//td[3]/text()')
      
      return i.load_item()
      
    def segment(text, url):
      response = http.TextResponse(url=url, body=str(text.replace(u'\xa0','')))
      s = XPathItemLoader(item=TCADSegmentItem(), response=response)
      
      s.add_xpath('improvement_id', '//td[1]/text()')
      s.add_xpath('id', '//td[2]/text()')
      s.add_xpath('type_code', '//td[3]/text()')
      s.add_xpath('description', '//td[4]/text()')
      s.add_xpath('klass', '//td[5]/text()')
      s.add_xpath('year_built', '//td[6]/text()')
      s.add_xpath('area', '//td[7]/text()')
      
      return s.load_item()
      
    def history(text, url):
      response = http.TextResponse(url=url, body=str(text.replace(u'\xa0','')))
      h = XPathItemLoader(item=TCADValueHistoryItem(), response=response)
      
      h.add_xpath('year', '//td[1]/text()')
      h.add_xpath('value', '//td[4]/text()')
      
      return h.load_item()
      
    hxs = HtmlXPathSelector(response)
    values = hxs.select('//font[text()="Improvement ID"]/../../../../tr[position()>1]').extract()
    parcel.add_value(
      'improvements', 
      map( improvement, values, [response.url,] * len(values) ) 
    )

    values = hxs.select('//font[text()="Imp ID"]/../../../../tr[position()>1 and position()<last()]').extract()
    parcel.add_value(
      'segments', 
      map( segment, values, [response.url,] * len(values) ) 
    )
    
    values = hxs.select('//td[text()="Certified Value History"]/../../../..//td[@colspan="5"]/following::tr[1]').extract()
    parcel.add_value(
      'historical_values', 
      map( history, values, [response.url,] * len(values) ) 
    )

    return parcel.load_item()
