import re
from datetime import *

from sqlalchemy import Table, Column, Integer, String, Float, Date, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from formencode import validators

Base = declarative_base()

class Rental(Base):
  __tablename__ = 'rental'
  
  def __init__(self, **props):
    for key in props.keys():
      if props[key] == '\xe2':
        props[key] = None
        
      if key == 'bathrooms':
        self.bathrooms, self.powder_rooms = props[key].re('(\d+) full, (\d+) partial|(\d+)')
      else:
        setattr(self, key, props[key])
      
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
  lot =           Column(String, nullable=True)
  year_built =    Column(Integer, nullable=True, index=True)
  lease_term =    Column(String, nullable=True)
  pets_allowed =  Column(String, nullable=True)
  date_listed =   Column(Date, nullable=True, index=True)
  mls_id =        Column(String, nullable=True)
  
  descriptive_title = Column(String, nullable=True)
  description =       Column(String, nullable=True)
  
  additional_fields = Column(String, nullable=True)
  
  public_records =    Column(String, nullable=True)
  
class Sale(Base):
  __tablename__ = 'for_sale'
  
  def __init__(self, **props):
    for key in props.keys():
      value = ( props[key][0] if isinstance( props[key], list ) else props[key] )
      
      if value == '\xe2':
        value = None
        
      if key == 'bathrooms':
        r = re.compile(r'(\d+) full, (\d+) partial')
        if r.search(value):
          ( self.bathrooms, self.powder_rooms ) = re.match(r'(\d+) full, (\d+) partial|(\d+)', value ).groups()
        else:
          self.bathrooms = value
      elif key == 'date_listed':
        self.date_listed = datetime.now() - timedelta( re.findall('(\d+) days ago', value) )
      elif key == 'price_per_sf':
        self.price_per_sf = value.strip('$')
      else:
        setattr(self, key, value)
  
  id = Column(Integer, primary_key=True)
  url = Column(String, index=True)
  address = Column(String)
  
  price =         Column(Float, index=True)
  bedrooms =      Column(Integer, nullable=True, index=True)
  bathrooms =     Column(Integer, nullable=True, index=True) 
  powder_rooms =  Column(Integer, nullable=True, index=True) 
  property_type = Column(String, nullable=True)
  size =          Column(Integer, nullable=True, index=True)
  lot =           Column(String, nullable=True)
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
  
