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
  __tablename__ = 'property'
  discriminator = Column('type', String(50)) 
  __mapper_args__ = {'polymorphic_on': discriminator}
    
  id = Column(Integer, primary_key=True)
  url = Column(String, index=True)
  address = Column(String)

  bedrooms =      Column(Integer, nullable=True, index=True)
  bathrooms =     Column(Float, nullable=True, index=True)
  powder_rooms =  Column(Integer, nullable=True, index=True) 
  property_type = Column(String, nullable=True)
  size =          Column(Integer, nullable=True, index=True)
  lot =           Column(Integer, nullable=True)
  year_built =    Column(Integer, nullable=True, index=True)
  date_listed =   Column(Date, nullable=True, index=True,)
  mls_id =        Column(String, nullable=True)

  descriptive_title = Column(String, nullable=True)
  description =       Column(String, nullable=True)

  additional_fields = Column(String, nullable=True)

  public_records =    Column(String, nullable=True)

  lat = Column(Float, nullable=True, index=True)
  lon = Column(Float, nullable=True, index=True)
  geom = GeometryColumn(Point(2), nullable=True)

  last_crawl = Column(DateTime)

  #tcad_2008_id = Column(Integer, ForeignKey('gis_schema.2008 TCAD Parcels.gid'))
  tcad_2008_id = Column(Integer, ForeignKey('2008 TCAD Parcels.gid'))
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
    else:
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
  #__table_args__ = {'schema':'gis_schema'}
  __mapper_args__ = {'polymorphic_identity': 'rental'}
  
  id = Column(Integer, ForeignKey('property.id'), primary_key=True)
  
  rent =          Column(Float, index=True)
  price_period =  Column(String, nullable=True)
  lease_term =    Column(String, nullable=True)
  pets_allowed =  Column(String, nullable=True)

  @validates('rent', 'price_period', 'lease_term', 'pets_allowed')
  def rental_validate_not_dash(self, key, value):
    return self.validate_not_dash(key,value)
  
  @validates('rent')
  def rental_validate_cost(self,key,value):
    return self.validate_cost(key,value)
    
class Listing(Property):
  __tablename__ = 'listing'
  #__table_args__ = {'schema':'gis_schema'}
  __mapper_args__ = {'polymorphic_identity': 'listing'}

  id = Column(Integer, ForeignKey('property.id'), primary_key=True)
  
  price       = Column(Float, index=True)
  sale_price  = Column(Integer, nullable=True, index=True)
  sale_date   = Column(Date, nullable=True)
  
  @validates('price', 'sale_price', 'sale_date')
  def listing_validate_not_dash(self, key, value):
    return self.validate_not_dash(key, value)
  
  @validates('price', 'sale_price')
  def listing_validate_cost(self, key, value):
    return self.validate_cost(key, value)
  
  @validates('sale_date')
  def listing_validate_date(self, key, value):
    return self.validate_date(key, value)
  
  @validates('price_per_sf')
  def listing_validate_number(self, key, value):
    return self.validate_number(key, value)

context_listing = Table('context_listing', Base.metadata,
    #Column('context_id', Integer, ForeignKey('gis_schema.context.id')),
    #Column('listing_id', Integer, ForeignKey('gis_schema.listing.id')),
    Column('context_id', Integer, ForeignKey('context.id')),
    Column('rental_id', Integer, ForeignKey('rental.id')),
    #schema = 'gis_schema', 
    useexisting=True
)
context_rental = Table('context_rental', Base.metadata,
    #Column('context_id', Integer, ForeignKey('gis_schema.context.id')),
    #Column('rental_id', Integer, ForeignKey('gis_schema.rental.id')),
    Column('context_id', Integer, ForeignKey('context.id')),
    Column('rental_id', Integer, ForeignKey('rental.id')),
    #schema = 'gis_schema', 
    useexisting=True
)

class Context(Base):
  __tablename__ = 'context'
  #__table_args__ = {'schema':'gis_schema'}
  
  id = Column(Integer, primary_key=True)
  
  name = Column(String, unique=True, index=True)

  geom = GeometryColumn(Polygon(2, srid=2277))
  
  listings = relationship("Listing",
                    secondary=context_listing,
                    backref="contexts")
  rentals = relationship("Rental",
                    secondary=context_rental,
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
  #__table_args__ = {'schema':'gis_schema'}  
  
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
  
class TCAD_2010(Base):
  __tablename__ = '2010 TCAD Parcels'
  #__table_args__ = {'schema':'gis_schema'}  
  __mapper_args__ = {'polymorphic_identity': '2010'}
  
  gid       = Column(Integer, primary_key=True)

  objectid  = Column(Integer, nullable=True)
  area      = Column(Numeric, nullable=True)
  plat      = Column(String, nullable=True)
  pid_10    = Column(String, nullable=True)   #TCAD Ref
  prop_id   = Column(Integer, nullable=True)  #TCAD ID
  lots      = Column(String, nullable=True)
  situs     = Column(String, nullable=True)   #Address Number
  blocks    = Column(String, nullable=True)
  condoid   = Column(String, nullable=True)
  condoid2  = Column(String, nullable=True)
  parcel_blo= Column(String, nullable=True)
  nbhd      = Column(String, nullable=True)
  zoning    = Column(String, nullable=True)
  land_value= Column(Numeric, nullable=True)
  grid      = Column(String, nullable=True)
  wcid17    = Column(String, nullable=True)
  shape_area= Column(Numeric, nullable=True)
  shape_len = Column(Numeric, nullable=True)
  the_geom  = GeometryColumn(Polygon(2, srid=2277 ))
  

  # Additional fields from TCAD scrape
  url               = Column(String, nullable=True)

  owner             = Column(String, nullable=True)
  owner_address     = Column(String, nullable=True)
  address           = Column(String, nullable=True)
  improvement_value = Column(Numeric, nullable=True)
  market_value      = Column(Numeric, nullable=True)
  acreage           = Column(Float, nullable=True)
  neighborhood      = Column(String, nullable=True)
      	
class TCADImprovement(Base):
  __tablename__ = 'TCAD_improvement'
  
  id = Column(Integer, primary_key=True)

  parcel_id = Column(Integer, ForeignKey('2010 TCAD Parcels.gid'))
  parcel = relationship("TCAD_2010", backref="improvements") 
    
  state_category    = Column(String, nullable=True)
  description       = Column(String, nullable=True)
  
class TCADSegment(Base):
  __tablename__ = 'TCAD_segment'
  
  id = Column(Integer, primary_key=True)
  
  improvement_id = Column(Integer, ForeignKey('TCAD_improvement.id'))
  improvement = relationship("TCADImprovement", backref="segments")  
  
  type_code         = Column(String, nullable=True)
  description       = Column(String, nullable=True)
  klass             = Column(String, nullable=True)
  year_built        = Column(Integer, nullable=True)
  area              = Column(Integer, nullable=True)
  
class TCADValueHistory(Base):
  __tablename__ = 'TCAD_value_history'
  
  id = Column(Integer, primary_key=True)
  
  parcel_id = Column(Integer, ForeignKey('2010 TCAD Parcels.gid'))
  parcel = relationship("TCADImprovement", backref="historical_values") 
  
  year              = Column(Integer, nullable=True)
  value             = Column(Numeric, nullable=True)
  
GeometryDDL(Property.__table__)
GeometryDDL(Context.__table__)
GeometryDDL(TCAD_2008.__table__)
GeometryDDL(TCAD_2010.__table__)
