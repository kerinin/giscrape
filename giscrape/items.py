# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
from scrapy.item import Item, Field

class TCADParcelItem(Item):
  url = Field()
  prop_id = Field()
  owner = Field()
  owner_address = Field()
  address = Field()
  
  land_value = Field()
  improvement_value = Field()
  market_value = Field()
  
  acreage = Field()
  neighborhood = Field()
  
  # Items
  improvements = Field()
  segments = Field()
  historical_values = Field()
  
class TCADImprovementItem(Item):
  id = Field()
  
  state_category = Field()
  description = Field()
  
class TCADSegmentItem(Item):
  id = Field()
  improvement_id = Field()
  
  type_code = Field()
  description = Field()
  klass = Field()
  year_built = Field()
  area = Field()
  
class TCADValueHistoryItem(Item):
  year = Field()
  value = Field()
  
class RentalItem(Item):
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
