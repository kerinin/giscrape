import re
from datetime import *

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from geoalchemy import *
from geoalchemy.geometry import Geometry

from orm import *
    
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
                    
  def cache_contents():
    session = Session()
    self.listings = []
    self.listings = session.query(Listing).filter(Listing.geom != None).filter( Listing.geom.transform(2277).within(self.geom.transform(2277))).all()
    
    self.rentals = []
    self.rentals = session.query(Rental).filter(Rental.geom != None).filter( Rental.geom.transform(2277).within(self.geom.transform(2277))).all()
    
    self.sales = []
    self.rentals = session.query(Sale).filter(Sale.geom != None).filter( Sale.geom.transform(2277).within(self.geom.transform(2277))).all()
    
GeometryDDL(Context.__table__)

