# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class SoldItem(Item):
  url = Field()
  address = Field()

  price = Field()
  bedrooms = Field()
  bathrooms = Field()
  powder_rooms = Field()
  property_type = Field()
  size = Field()
  lot = Field()
  price_per_sf = Field()
  year_built = Field()

  public_records = Field()

  sale_date = Field()

class SaleItem(Item):
  url = Field()
  address = Field()
  
  price = Field()
  bedrooms = Field()
  bathrooms = Field()
  powder_rooms = Field()
  property_type = Field()
  size = Field()
  lot = Field()
  price_per_sf = Field()
  year_built = Field()
  date_listed = Field()
  mls_id = Field()
  
  descriptive_title = Field()
  description = Field()
  
  additional_fields = Field()
  
  fees = Field()
  
  public_records = Field()
  property_taxes = Field()
  
  sale_price = Field()
  sale_date = Field()
