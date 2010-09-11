# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class RentalItem(Item):
  # define the fields for your item here like:
  # name = Field()
  url = Field()
  address = Field()
  
  price = Field()
  price_period = Field()
  bedrooms = Field()
  bathrooms = Field()
  property_type = Field()
  size = Field()
  lot = Field()
  year_built = Field()
  lease_term = Field()
  pets_allowed = Field()
  date_listed = Field()
  mls_id = Field()
  
  descriptive_title = Field()
  description = Field()
  
  additional_fields = Field()
  
  public_records = Field()
    
    
class SaleItem(Item):
  url = Field()
  address = Field()
  
  price = Field()
  bedrooms = Field()
  bathrooms = Field()
  property_type = Field()
  size = Field()
  lot = Field()
  price_per_sf = Field()
  year_built = Field()
  date_listed = Field()
  mls_id = Field()
  
  description = Field()
  
  additional_fields = Field()
  
  fees = Field()
  
  public_records = Field()
  property_taxes = Field()
  
  sale_price = Field()
  sale_date = Field()
