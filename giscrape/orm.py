import re
from datetime import *

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from geoalchemy import *

engine = create_engine('postgresql://postgres:kundera2747@localhost/gisdb')
metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)
Session = sessionmaker(bind=engine)
global DefaultDialect
DefaultDialect = engine.dialect

class Fail(StandardError):
  pass
  
def init(self, **props):
  for key in props.keys():
    value = ( props[key][0] if isinstance( props[key], list ) else props[key] )
    value = value[0] if isinstance(value,list) else value
    
    if value == '\xe2':
      value = None
      
    if key == 'date_listed':
      self.date_listed = None if (value == '180+ days ago') else datetime.now() - timedelta( int( re.findall('(\d+) days ago', value)[0] ) )
    elif key == 'price_per_sf' or key == 'size':
      setattr(self, key, int( value.replace(',','').strip('$') ) )
    elif key == 'price':
      if re.search(r'\xe2', value) or value.count(u'\u2013'): raise Fail, "Price span"
      
      self.price = re.findall(r'\$([\d|,]+)', value)[0].replace(',','').strip('$')
    elif key == 'lot':
      by_sf = re.compile(r'([\d|,]+) sqft')
      by_acre = re.compile(r'([\d|,|.]+) acres')
      if by_sf.search(value):
        self.lot = by_sf.findall(value)[0].replace(',','')
      elif by_acre.search(value):
        self.lot = int( 43560.0 * float( by_acre.findall(value)[0].replace(',','') ) )
    elif key == 'sale_date':
      self.sale_date = datetime.strptime(value.replace('st','').replace('nd','').replace('rd','').replace('th',''),'%b %d, %Y')
    elif key == 'address' and 'Address Not Disclosed' in value:
      pass
    else:
      setattr(self, key, value)
     
class Rental(Base):
  __tablename__ = 'rental'
  __table_args__ = {'schema':'gis_schema'}
    
  def __init__(self, **props):
    init(self,**props)

  def update(self, **props):
    init(self,**props)
        
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
  
  lat = Column(Float, nullable=True, index=True)
  lon = Column(Float, nullable=True, index=True)
  geom = GeometryColumn(Point(2), nullable=True)
  
  last_crawl = Column(DateTime)
  
  tcad_2008_id = Column(Integer, ForeignKey('gis_schema.2008 TCAD Parcels.gid'))
  tcad_2008_parcel = relationship("TCAD_2008", backref="rentals")  
  
class Listing(Base):
  __tablename__ = 'listing'
  __table_args__ = {'schema':'gis_schema'}
  
  def __init__(self, **props):
    init(self,**props)

  def update(self, **props):
    init(self,**props)
    
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
  
  lat = Column(Float, nullable=True, index=True)
  lon = Column(Float, nullable=True, index=True)
  geom = GeometryColumn(Point(2), nullable=True)
  
  last_crawl = Column(DateTime)
  
  tcad_2008_id = Column(Integer, ForeignKey('gis_schema.2008 TCAD Parcels.gid'))
  tcad_2008_parcel = relationship("TCAD_2008", backref="listings")  
  
class Sale(Base):
  __tablename__ = 'sale'
  __table_args__ = {'schema':'gis_schema'}

  def __init__(self, **props):
    init(self,**props)

  def update(self, **props):
    init(self,**props)
			
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

  public_records =    Column(String, nullable=True)

  fees = Column(String, nullable=True)

  public_records = Column(String, nullable=True)

  sale_date = Column(Date, nullable=True)

  lat = Column(Float, nullable=True, index=True)
  lon = Column(Float, nullable=True, index=True)
  geom = GeometryColumn(Point(2), nullable=True)

  last_crawl = Column(DateTime)
  
  tcad_2008_id = Column(Integer, ForeignKey('gis_schema.2008 TCAD Parcels.gid'))
  tcad_2008_parcel = relationship("TCAD_2008", backref="sales")  

context_listing = Table('context_listing', Base.metadata,
    Column('context_id', Integer, ForeignKey('gis_schema.context.id')),
    Column('listing_id', Integer, ForeignKey('gis_schema.listing.id')),
    schema = 'gis_schema', useexisting=True
)
context_rental = Table('context_rental', Base.metadata,
    Column('context_id', Integer, ForeignKey('gis_schema.context.id')),
    Column('rental_id', Integer, ForeignKey('gis_schema.rental.id')),
    schema = 'gis_schema', useexisting=True
)
context_sale = Table('context_sale', Base.metadata,
    Column('context_id', Integer, ForeignKey('gis_schema.context.id')),
    Column('sale_id', Integer, ForeignKey('gis_schema.sale.id')),
    schema = 'gis_schema', useexisting=True
)

class Context(Base):
  __tablename__ = 'context'
  __table_args__ = {'schema':'gis_schema'}
  
  id = Column(Integer, primary_key=True)
  
  name = Column(String, unique=True, index=True)

  geom = GeometryColumn(Polygon(2, srid=2277))
  
  listings = relationship("Listing",
                    secondary=context_listing,
                    backref="contexts")
  rentals = relationship("Rental",
                    secondary=context_rental,
                    backref="contexts")  
  sales = relationship("Sale",
                    secondary=context_sale,
                    backref="contexts") 
                    
  def cache_contents(self,session):
    self.listings = []
    self.listings = session.query(Listing).filter(Listing.geom != None).filter( Listing.geom.transform(2277).within(self.geom.transform(2277))).all()
    
    self.rentals = []
    self.rentals = session.query(Rental).filter(Rental.geom != None).filter( Rental.geom.transform(2277).within(self.geom.transform(2277))).all()
    
    self.sales = []
    self.rentals = session.query(Sale).filter(Sale.geom != None).filter( Sale.geom.transform(2277).within(self.geom.transform(2277))).all()
    
class TCAD_2008(Base):
  __tablename__ = '2008 TCAD Parcels'
  __table_args__ = {'schema':'gis_schema'}
  
  gid           = Column(Integer, primary_key=True)
  acreage       = Column(Float, nullable=True)
  roads         = Column(String, nullable=True)
  water         = Column(String, nullable=True)
  ag_land       = Column(String, nullable=True)
  vli_2005      = Column(String, nullable=True)
  vli_2008      = Column(String, nullable=True)
  pct_impr      = Column(String, nullable=True)
  geo_id        = Column(String, nullable=True)
  land_state    = Column(String, nullable=True)
  marketvalu    = Column(Integer, nullable=True)
  shape_leng    = Column(Numeric, nullable=True)
  shape_area    = Column(Numeric, nullable=True)
  improvemen    = Column(Integer, nullable=True)
  land_value    = Column(Integer, nullable=True)
  value_per_acre= Column(Integer, nullable=True)
  the_geom      = GeometryColumn(Polygon(2, srid=2277 ))
  
	
GeometryDDL(Listing.__table__)
GeometryDDL(Rental.__table__)
GeometryDDL(Sale.__table__)
GeometryDDL(Context.__table__)
