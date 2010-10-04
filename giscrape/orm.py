from sqlalchemy import Table, Column, Integer, String, Float, Date, MetaData, ForeignKey

metadata = MetaData()

rental_table = Table('rental', metadata,
  Column('id', Integer, primary_key=True),
  Column('url', String, unique=True, index=True),
  Column('address', String),
  
  Column('price', Float, index=True),
  Column('price_period', String, nullable=True),
  Column('bedrooms', Integer, nullable=True, index=True),
  Column('bathrooms', Float, nullable=True, index=True),
  Column('property_type', String, nullable=True),
  Column('size', Integer, nullable=True, index=True),
  Column('lot', String, nullable=True),
  Column('year_built', Integer, nullable=True, index=True),
  Column('lease_term', String, nullable=True),
  Column('pets_allowed', String, nullable=True),
  Column('date_listed', Date, nullable=True, index=True),
  Column('mls_id', String, nullable=True),
  
  Column('descriptive_title', String, nullable=True),
  Column('description', String, nullable=True),
  
  Column('additional_fields', String, nullable=True),
  
  Column('public_records', String, nullable=True)
  )
  
sale_table = Table('for_sale', metadata,
  Column('id', Integer, primary_key=True),
  Column('url', String, unique=True, index=True),
  Column('address', String),
  
  Column('price', Float, index=True),
  Column('bedrooms', Integer, nullable=True, index=True),
  Column('bathrooms', Float, nullable=True, index=True),
  Column('property_type', String, nullable=True),
  Column('size', Integer, nullable=True, index=True),
  Column('lot', String, nullable=True),
  Column('price_per_sf', Float, nullable=True, index=True),
  Column('year_built', Integer, nullable=True, index=True),
  Column('date_listed', Date, nullable=True, index=True),
  Column('mls_id', String, nullable=True),
  
  Column('descriptive_title', String, nullable=True),
  Column('description', String, nullable=True),
  
  Column('additional_fields', String, nullable=True),
  
  Column('fees', String, nullable=True),
  
  Column('public_records', String, nullable=True),
  Column('property_taxes', String, nullable=True),
  
  Column('sale_price', Integer, nullable=True, index=True),
  Column('sale_date', Date, nullable=True)
  )
