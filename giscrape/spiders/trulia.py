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
    
class TruliaSpider(CrawlSpider):
  name = 'trulia'
  allowed_domains = ['www.trulia.com']

  start_urls = [
      "http://www.trulia.com/for_sale/Austin,TX/",
      "http://www.trulia.com/for_rent/Austin,TX/",
			"http://www.trulia.com/sold/Austin,TX/",
  ]
  
  rules = (
    Rule( SgmlLinkExtractor(restrict_xpaths='//a[@class="pg_link"]') ),
    Rule( customExtractor(allow='www.trulia.com/rental'),callback='parse_rental' ),
    Rule( customExtractor(allow='www.trulia.com/property'),callback='parse_listing' ),
		Rule( customExtractor(allow='http://www.trulia.com/homes/Texas/Austin/sold'),callback='parse_sale' ),
  )
  
  def parse_sale(self, response):
    l = XPathItemLoader(item=SaleItem(), response=response)

    l.add_value('url', response.url)
    l.add_xpath('address', '//h1[@class="address"]/text()')

    l.add_xpath('price', '//div[@class="price"]/text()')
    l.add_xpath('sale_date', '//th[text()="Last sale:"]/../td/div[last()]/text()', re=r'on (\w+)')

    l.add_xpath('bedrooms', '//th[text()="Bedrooms:"]/../td/text()')
    l.add_xpath('bathrooms', '//th[text()="Bathrooms:"]/../td/text()', re=r'(\d+)')
    l.add_xpath('powder_rooms', '//th[text()="Bathrooms:"]/../td/text()', re=r', (\d+)')
    l.add_xpath('property_type', '//th[text()="Property type:"]/../td/text()')
    l.add_xpath('size', '//th[text()="Size:"]/../td/text()', re=r'([\d|,]+) sqft')
    l.add_xpath('lot', '//th[text()="Lot:"]/../td/text()')
    l.add_xpath('price_per_sf', '//th[text()="Price/sqft:"]/../td/text()')
    l.add_xpath('year_built', '//th[text()="Year built:"]/../td/text()')

    l.add_xpath('public_records', 'id("property_public_info_module")/ul/li/span/text()')

    return l.load_item()

  def parse_rental(self, response):
    l = XPathItemLoader(item=RentalItem(), response=response)
    
    l.add_value('url', response.url)
    l.add_xpath('address', '//th[text()="Address:"]/../td/text()')
    
    l.add_xpath('price', '//th[text()="Price:"]/../td/div/text()')
    l.add_xpath('price_period', '//th[text()="Price:"]/../td/div/span/text()')
    
    l.add_xpath('bedrooms', '//th[text()="Bedrooms:"]/../td/text()')
    l.add_xpath('bathrooms', '//th[text()="Bathrooms:"]/../td/text()', re=r'(\d+)')
    l.add_xpath('powder_rooms', '//th[text()="Bathrooms:"]/../td/text()', re=r', (\d+)')
    l.add_xpath('property_type', '//th[text()="Property type:"]/../td/text()')
    l.add_xpath('size', '//th[text()="Size:"]/../td/text()', re=r'([\d|,]+) sqft')
    l.add_xpath('lot', '//th[text()="Lot:"]/../td/text()')
    l.add_xpath('year_built', '//th[text()="Year built:"]/../td/text()')
    l.add_xpath('lease_term', '//th[text()="Terms of lease:"]/../td/text()')
    l.add_xpath('pets_allowed', '//th[text()="Pets:"]/../td/text()')
    l.add_xpath('date_listed', '//th[text()="Added on Trulia:"]/../td/text()')
    l.add_xpath('mls_id', '//th[text()="MLS/ID:"]/../td/text()')
    
    l.add_xpath('descriptive_title', '//h2[@class="descriptive_title"]/text()')
    l.add_xpath('description', '//div[@class="listing_description_module"]/text()')
    
    l.add_xpath('additional_fields', 'id("property_listing_details_module")/ul/li/span/text()')
    
    l.add_xpath('public_records', 'id("property_public_info_module")/ul/li/span/text()')
    
    return l.load_item()
    
  def parse_listing(self, response):
    l = XPathItemLoader(item=ListingItem(), response=response)
    
    l.add_value('url', response.url)
    l.add_xpath('address', '//h1[@class="address"]/text()')
    
    l.add_xpath('price', '//div[@class="price"]/text()')

    l.add_xpath('bedrooms', '//th[text()="Bedrooms:"]/../td/text()')
    l.add_xpath('bathrooms', '//th[text()="Bathrooms:"]/../td/text()', re=r'(\d+)')
    l.add_xpath('powder_rooms', '//th[text()="Bathrooms:"]/../td/text()', re=r', (\d+)')
    l.add_xpath('property_type', '//th[text()="Property type:"]/../td/text()')
    l.add_xpath('size', '//th[text()="Size:"]/../td/text()', re=r'([\d|,]+) sqft')
    l.add_xpath('lot', '//th[text()="Lot:"]/../td/text()')
    l.add_xpath('price_per_sf', '//th[text()="Price/sqft:"]/../td/text()')
    l.add_xpath('year_built', '//th[text()="Year built:"]/../td/text()')
    l.add_xpath('date_listed', '//th[text()="Added on Trulia:"]/../td/text()')
    l.add_xpath('mls_id', '//th[text()="MLS/ID:"]/../td/text()')
    
    l.add_xpath('descriptive_title', '//h2[@class="descriptive_title"]/text()')
    l.add_xpath('description', '//div[@class="listing_description_module"]/text()')
    
    l.add_xpath('additional_fields', 'id("property_listing_details_module")/ul/li/span/text()')
    
    l.add_xpath('public_records', 'id("property_public_info_module")/ul/li/span/text()')

    return l.load_item()
