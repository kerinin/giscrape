import re
from datetime import *

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy import *

from orm import *

context_listing = Table('context_listing', Base.metadata,
    Column('context_id', Integer, ForeignKey('context.id')),
    Column('listing_id', Integer, ForeignKey('listing.id'))
)
context_rental = Table('context_rental', Base.metadata,
    Column('context_id', Integer, ForeignKey('context.id')),
    Column('rental_id', Integer, ForeignKey('rental.id'))
)
context_sale = Table('context_sale', Base.metadata,
    Column('context_id', Integer, ForeignKey('context.id')),
    Column('sale_id', Integer, ForeignKey('sale.id'))
)

class Context(Base):
  __tablename__ = 'context'
  __table_args__ = {'schema':'gis_schema'}
  
  id = Column(Integer, primary_key=True)
  
  name = Colum(String, unique=True, index=True)

  geom = GeometryColumn(Polygon(2), srid=2277)
  
  listings = relationship("Listing",
                    secondary=context_listing,
                    backref="contexts")
  rentals = relationship("Rental",
                    secondary=context_rental,
                    backref="contexts")  
  sales = relationship("Sale",
                    secondary=context_sale,
                    backref="contexts") 
