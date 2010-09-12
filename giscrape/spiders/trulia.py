import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor, BaseSgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from giscrape.items import *
from scrapy.item import Item, Field

class TruliaSpider(CrawlSpider):
  name = 'trulia'
  allowed_domains = ['www.trulia.com']

  start_urls = [
      "http://www.trulia.com/for_sale/Austin,TX/",
      "http://www.trulia.com/for_rent/Austin,TX/",
  ]
  
  rules = (
    Rule( SgmlLinkExtractor(restrict_xpaths='//a[@class="pg_link"]') ),
    Rule( SgmlLinkExtractor(allow='www.trulia.com/rental'),callback='parse_for_rental' ),
    Rule( SgmlLinkExtractor(allow='www.trulia.com/property'),callback='parse_for_sale' ),
  )
        
  def parse_rental(self, response):
    hxs = HtmlXPathSelector(response)
    
    rental = RentalItem()
    rental['url'] = response.url
    rental['address'] = hxs.select('//h1[@class="address"]/text()').extract()
    
    rental['price'] = hxs.select('//div[@class="price"]/text()[1]').re(r'$(\n+)')
    rental['price_period'] = hxs.select('//div[@class="price"]/span[@class="normal"]/text()').extract()

    rental['bedrooms'] = hxs.select('//th[text()="Bedrooms:"]/../td/text()').extract()
    rental['bathrooms'] = hxs.select('//th[text()="Bathrooms:"]/../td/text()').extract()
    rental['property_type'] = hxs.select('//th[text()="Property type:"]/../td/text()').extract()
    rental['size'] = hxs.select('//th[text()="Size:"]/../td/text()').re(r'\n+')
    rental['lot'] = hxs.select('//th[text()="Lot:"]/../td/text()').extract()
    rental['year_built'] = hxs.select('//th[text()="Year built:"]/../td/text()').extract()
    rental['lease_term'] = hxs.select('//th[text()="Terms of lease:"]/../td/text()').extract()
    rental['pets_allowed'] = hxs.select('//th[text()="Pets:"]/../td/text()').extract()
    rental['date_listed'] = hxs.select('//th[text()="Added on Trulia:"]/../td/text()').extract()
    rental['mls_id'] = hxs.select('//th[text()="MLS/ID:"]/../td/text()').extract()
    
    rental['descriptive_title'] = hxs.select('//h2[@class="descriptive_title"]/text()').extract()
    rental['description'] = hxs.select('//div[@class="listing_description_module"]/text()').extract()
    
    rental['additional_fields'] = hxs.select('id("property_listing_details_module")/ul/li/span/text()').extract()
    
    rental['public_records'] = hxs.select('id("property_public_info_module")/ul/li/span/text()').extract()
    
    return rental
