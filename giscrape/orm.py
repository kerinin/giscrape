import re
from datetime import *

from sqlalchemy import Table, Column, Integer, String, Float, Date, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from formencode import validators

Base = declarative_base()

class Instantiator:
  def __init__(self, **props):
    for key in props.keys():
      value = ( props[key][0] if isinstance( props[key], list ) else props[key] )
      
      if value == '\xe2':
        value = None
        
      if key == 'date_listed':
        self.date_listed = None if (value == '180+ days ago') else datetime.now() - timedelta( int( re.findall('(\d+) days ago', value)[0] ) )
      elif key == 'price_per_sf' or key == 'price' or key == 'size':
        setattr(self, key, value.replace(',','').strip('$') )
      elif key == 'lot':
        by_sf = re.compile(r'([\d|,]+) sqft')
        by_acre = re.compile(r'([\d|,|.]+) acres')
        if by_sf.search(value):
          self.lot = by_sf.findall(value)[0]
        elif by_acre.search(value):
          self.lot = int( 43560.0 * float( by_acre.findall(value)[0].replace(',','') ) )
      elif key == 'address' and 'Address Not Disclosed' in value:
        pass
      else:
        setattr(self, key, value)
        
class Rental(Base, Instantiator):
  __tablename__ = 'rental'
    
  id = Column(Integer, primary_key=True)
  url = Column(String, index=True)
  address = Column(String)
  
  price =         Column(Float, index=True)
  price_period =  Column(String, nullable=True)
  bedrooms =      Column(Integer, nullable=True, index=True)
  bathrooms =     Column(Float, nullable=True, index=True)
  powder_rooms =  Column(Integer, nullable=True, index=True) 
  property_type = Column(String, nullable=True)
  size =          Column(Integer, nullable=True, index=True)
  lot =           Column(Integer, nullable=True)
  year_built =    Column(Integer, nullable=True, index=True)
  lease_term =    Column(String, nullable=True)
  pets_allowed =  Column(String, nullable=True)
  date_listed =   Column(Date, nullable=True, index=True)
  mls_id =        Column(String, nullable=True)
  
  descriptive_title = Column(String, nullable=True)
  description =       Column(String, nullable=True)
  
  additional_fields = Column(String, nullable=True)
  
  public_records =    Column(String, nullable=True)
  
class Sale(Base, Instantiator):
  __tablename__ = 'for_sale'
  
  id = Column(Integer, primary_key=True)
  url = Column(String, index=True)
  address = Column(String)
  
  price =         Column(Float, index=True)
  bedrooms =      Column(Integer, nullable=True, index=True)
  bathrooms =     Column(Integer, nullable=True, index=True) 
  powder_rooms =  Column(Integer, nullable=True, index=True) 
  property_type = Column(String, nullable=True)
  size =          Column(Integer, nullable=True, index=True)
  lot =           Column(Integer, nullable=True)
  price_per_sf =  Column(Float, nullable=True, index=True)
  year_built =    Column(Integer, nullable=True, index=True)
  date_listed =   Column(Date, nullable=True, index=True)
  mls_id =        Column(String, nullable=True)
  
  descriptive_title = Column(String, nullable=True)
  description =       Column(String, nullable=True)
  
  additional_fields = Column(String, nullable=True)
  
  public_records =    Column(String, nullable=True)
  
  fees = Column(String, nullable=True)
  
  public_records = Column(String, nullable=True)
  property_taxes = Column(String, nullable=True)
  
  sale_price = Column(Integer, nullable=True, index=True)
  sale_date = Column(Date, nullable=True)
  
