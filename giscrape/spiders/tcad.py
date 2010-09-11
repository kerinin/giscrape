from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from items import RentalItem, SaleItem

class TCADSpider(CrawlSpider):
  name = "tcad"
  allowed_domains = ["www.traviscad.org/"]
  # The best approach is probably going to be to select a few thousand property
  # ID's from the database and construct a set of URL's.  The query can be for
  # last updated first
  start_urls = [
  ]
  
  rules = (
  )
  
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    
    return items
