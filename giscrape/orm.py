import re
from datetime import *

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy.orm.interfaces import *
from geoalchemy import *

engine = create_engine('postgresql://postgres:kundera2747@localhost/gisdb')
metadata = MetaData(engine)
Base = declarative_base(metadata=metadata)
Session = sessionmaker(bind=engine)
global DefaultDialect
DefaultDialect = engine.dialect

class Fail(StandardError):
  pass
     
class Property(Base):
  id = Column(Integer, primary_key=True)
  url = Column(String, index=True)
  address = Column(String)

  bedrooms =      Column(Integer, nullable=True, index=True)
  bathrooms =     Column(Float, nullable=True, index=True)
  powder_rooms =  Column(Integer, nullable=True, index=True) 
  property_type = Column(String, nullable=True)
  size =          Column(Integer, nullable=True, index=True, extension = Number())
  lot =           Column(Integer, nullable=True, extension = Lot())
  year_built =    Column(Integer, nullable=True, index=True)
  date_listed =   Column(Date, nullable=True, index=True, extension = Date())
  mls_id =        Column(String, nullable=True)

  descriptive_title = Column(String, nullable=True)
  description =       Column(String, nullable=True, extension = Paragraph)

  additional_fields = Column(String, nullable=True, extension = Paragraph)

  public_records =    Column(String, nullable=True, extension = Paragraph)

  lat = Column(Float, nullable=True, index=True)
  lon = Column(Float, nullable=True, index=True)
  geom = GeometryColumn(Point(2), nullable=True)

  last_crawl = Column(DateTime)

  tcad_2008_id = Column(Integer, ForeignKey('gis_schema.2008 TCAD Parcels.gid'))
  tcad_2008_parcel = relationship("TCAD_2008", backref="rentals")  
  
  @validates('bedrooms', 'bathrooms', 'powder_rooms', 'property_type', 'size', 'lot', 'year_built', 'date_listed', 'mls_id')
  def validate_not_dash(self, key, value):
    if value == '\xe2': return None
    return value
    
  @validates('date_listed')
  def validate_date(self, key, value):
    if (value == '180+ days ago'):
      return None 
    elif re.search('(\d+) days ago'):
      return datetime.now() - timedelta( int( re.findall('(\d+) days ago', value)[0] ) )
   else
      return datetime.strptime(value.replace('st','').replace('nd','').replace('rd','').replace('th',''),'%b %d, %Y')

  @validates('size')
  def validate_number(self, key, value):
    return value.replace(',','').strip('$')
    
  @validates('lot')
  def validate_area(self, key, value):
    by_sf = re.compile(r'([\d|,]+) sqft')
    by_acre = re.compile(r'([\d|,|.]+) acres')
    if by_sf.search(value):
      return by_sf.findall(value)[0].replace(',','')
    elif by_acre.search(value):
      return int( 43560.0 * float( by_acre.findall(value)[0].replace(',','') ) )
    
  @validates('address')
  def validate_address(self, key, value):
    if 'Address Not Disclosed' in value: return None
    return value
    
  def validate_cost(self, key, value):
    if re.search(r'\xe2', value) or value.count(u'\u2013'): raise Fail, "Price span"
    
    return re.findall(r'\$([\d|,]+)', value)[0].replace(',','').strip('$')
    
  @validates('description', 'additional_fields', 'public_records')
  def validate_paragraph(self, key, value):
    return value.concat() if isinstance(value, list) else value
    
class Rental(Property):
  __tablename__ = 'rental'
  __table_args__ = {'schema':'gis_schema'}
  __mapper_args__ = {'concrete':True}

  rent =          Column(Float, index=True)
  price_period =  Column(String, nullable=True)
  lease_term =    Column(String, nullable=True)
  pets_allowed =  Column(String, nullable=True)

  @validates('rent', 'price_period', 'lease_term', 'pets_allowed')
  validate_not_dash
  
  @validates('rent')
  validate_cost
    
class Listing(Base):
  __tablename__ = 'listing'
  __table_args__ = {'schema':'gis_schema'}
  __mapper_args__ = {'concrete':True}

  price =         Column(Float, index=True)
  sale_price = Column(Integer, nullable=True, index=True)
  sale_date = Column(Date, nullable=True)
  
  @validates('price', 'sale_price', 'sale_date')
  validate_not_dash
  
  @validates('price', 'sale_price')
  validate_cost
  
  @validates('sale_date')
  validate_date
  
  @validates('price_per_sf')
  validate_number

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
    
class TCAD(Base):
  __tablename__ = '2008 TCAD Parcels'
  __table_args__ = {'schema':'gis_schema'}
  
  # COA GIS fields
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
  
class TCAD_2008(TCAD):
  __tablename__ = '2008 TCAD Parcels'
  __table_args__ = {'schema':'gis_schema'}  
  __mapper_args__ = {'concrete':True}

class TCAD_2010(TCAD):
  __tablename__ = '2008 TCAD Parcels'
  __table_args__ = {'schema':'gis_schema'}  
  __mapper_args__ = {'concrete':True}

  # Additional fields from TCAD scrape
  url           = Column(String, nullable=True)
  parcel_id     = Column(Integer, nullable=True)
  address       = Column(String, nullable=True)
  neighborhood  = Column(String, nullable=True)
      	
GeometryDDL(Listing.__table__)
GeometryDDL(Rental.__table__)
GeometryDDL(Sale.__table__)
GeometryDDL(Context.__table__)
