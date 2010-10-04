from sqlalchemy import Table, Column, Integer, String, Float, Date, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Rental(Base):
  __tablename__ = 'rental'
  
  def __init__(self, **props):
    for key in props.keys():
      setattr(self, key, props[key])
      
  id = Column(Integer, primary_key=True)
  url = Column(String, unique=True, index=True)
  address = Column(String)
  
  price =         Column(Float, index=True)
  price_period =  Column(String, nullable=True)
  bedrooms =      Column(Integer, nullable=True, index=True)
  bathrooms =     Column(Float, nullable=True, index=True)
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
      setattr(self, key, props[key])
  
  id = Column(Integer, primary_key=True)
  url = Column(String, unique=True, index=True)
  address = Column(String)
  
  price =         Column(Float, index=True)
  bedrooms =      Column(Integer, nullable=True, index=True)
  bathrooms =     Column(Float, nullable=True, index=True)
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
  
