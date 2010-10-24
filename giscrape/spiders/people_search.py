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

def isDefined(x):
  if x['first'] and x['last'] and ((x['city'] and x['state']) or x['zipcode']): return 1
  else: return 0

def parse_owner(parcel):
  first = middle = last = None
  
  if re.search('^(\w+) (\w+)$', parcel.owner):
    last, first = re.findall( '(\w+) (\w+)',parcel.owner )[0]
  elif re.search('^(\w+) (\w+) (\w+)$', parcel.owner):
    last, first, middle = re.findall( '(\w+) (\w+) (\w+)',parcel.owner )[0]
  elif re.search('^(\w+) (\w+) &amp; (\w+)$', parcel.owner):
    last, first = re.findall( '(\w+) (\w+)',parcel.owner )[0]
  elif re.search('^(\w+) (\w+) (\w+) &amp: (\w+)$', parcel.owner):
    last, first, middle = re.findall( '(\w+) (\w+) (\w+)',parcel.owner )[0]
  elif re.search('^(\w+) (\w+) &amp; (\w+) (\w+)$', parcel.owner):
    last, first = re.findall( '(\w+) (\w+)',parcel.owner )[0]
  elif re.search('^(\w+) (\w+) (\w+) &amp: (\w+) (\w+)$', parcel.owner):
    last, first, middle = re.findall( '(\w+) (\w+) (\w+)',parcel.owner )[0]
  elif re.search('^(\w+) (\w+) &amp; (\w+) (\w+) (\w+)$', parcel.owner):
    last, first = re.findall( '(\w+) (\w+)',parcel.owner )[0]
  elif re.search('^(\w+) (\w+) (\w+) &amp: (\w+) (\w+) (\w+)$', parcel.owner):
    last, first, middle = re.findall( '(\w+) (\w+) (\w+)', parcel.owner	 )[0]
  
  if re.search('(\w+), \w{2} \d{5}-\d{4}', parcel.owner_address):
    city = re.findall('(\w+), \w{2} \d{5}-\d{4}', parcel.owner_address)[0]
  else:
    city = None
  if re.search('\w+, (\w+) \d{5}-\d{4}', parcel.owner_address):
    state = re.findall('\w+, (\w+) \d{5}-\d{4}', parcel.owner_address)[0]
  else:
    state = None
  if re.search('\w+, \w{2} (\d+)-\d{4}', parcel.owner_address):
    zipcode = re.findall('\w+, \w{2} (\d+)-\d{4}', parcel.owner_address)[0]
  else:
    zipcode = None
  
  return { 'first':first, 'middle':middle, 'last':last, 'city':city, 'state':state, 'zipcode':zipcode, 'prop_ref':parcel.objectid }
  
        
class customExtractor(SgmlLinkExtractor):
  def extract_links(self, response):
    response.body = response.body.replace('\\','')
    return SgmlLinkExtractor.extract_links(self,response)
    
class TcadSpider(BaseSpider):
  name = 'people_search'
  allowed_domains = ['http://www.peoplelookup.com/']

  session = Session()
  shady = WKTSpatialElement("POINT(%s %s)" % (-97.699009500000003, 30.250421899999999) )
  
  people = [ parse_owner(x) for x in session.query(TCAD_2010).filter(TCAD_2010.owner != None).order_by(TCAD_2010.the_geom.centroid().distance(shady.transform(2277))).all() ]
  people = filter(isDefined,people)
  
  urls = [ "http://www.peoplelookup.com/results.php?ReportType=1&qf=%s&qmi=%s&qn=%s&qc=%s&qz=%s&qs=%s&focusfirst=1&prop_ref=%s" % (x['first'], x['middle'], x['last'], x['city'], x['zipcode'], x['state'], x['prop_ref']) for x in people ]
  urls.reverse()
  start_urls = urls
  
  def parse(self, response):
    response.body = response.body.replace('\\','').replace('\xa0','')
    p = XPathItemLoader(item=PersonItem(), response=response)
    
    try:
      p.add_value('first_name', re.findall( '&qf=(\w+)&', response.url )[0] )
      p.add_value('middle_name', re.findall( '&qmi=(\w+)&', response.url )[0] )
      p.add_value('last_name', re.findall( '&qn=(\w+)&', response.url )[0] )
      p.add_value('city', re.findall( '&qc=(\w+)&', response.url )[0] )
      p.add_value('state', re.findall( '&qs=(\w+)&', response.url )[0] )
      p.add_value('zipcode', re.findall( '&qz=(\d+)&', response.url )[0] )
      p.add_value('prop_ref', re.findall( '&prop_ref=(\d+)', response.url )[0] )
      
      p.add_xpath('cities', '//div[@class="addresses"]/p/b/text()[1]', re="([^\(]+)")
      p.add_xpath('age','//div[@class="greenTopBoxLeft round12_12_0_0"]/p[@class="nameAge"]/text()[2]', re=", Age (\d+)")
    except IndexError:
      pass
    else:
      return p.load_item()
