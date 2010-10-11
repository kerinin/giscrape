# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TCADParcelItem(Item):
  # define the fields for your item here like:
  # name = Field()
  url = Field()
  parcel_id = Field()
  address = Field()
  
  land_value = Field()
  improvement_value = Field()
  total_value = Field()
  
  land_acres = Field()
  neighborhood = Field()
  
  # Items
  improvements = Field()
  segments = Field()
  value_history = Field()
  
class TCADImprovementItem(Item):
  improvement_id = Field()
  
  category = Field()
  description = Field()
  
class TCADSegmentItem(Item):
  improvement_id = Field()
  segment_id = Field()
  
  type_code = Field()
  description = Field()
  klass = Field()
  year_built = Field()
  area = Field()
  
class TCADValueHistoryItem(Item):
  parcel_id = Field()
  
  year = Field()
  value = Field()
  
class RentalItem(Item):
  # define the fields for your item here like:
  # name = Field()
  url = Field()
  address = Field()
  
  price = Field()
  price_period = Field()
  bedrooms = Field()
  bathrooms = Field()
  powder_rooms = Field()
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
  powder_rooms = Field()
  property_type = Field()
  size = Field()
  lot = Field()
  price_per_sf = Field()
  year_built = Field()

  public_records = Field()

  sale_date = Field()

class ListingItem(Item):
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
