#! /usr/bin/env python

import sys, getopt, math, datetime, os
import locale

from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql.expression import *

from giscrape import orm
from giscrape.orm import *

from geopy import geocoders
from geopy.geocoders.google import *

_Functions = ['run']
	
engine = create_engine('postgresql://postgres:kundera2747@localhost/gisdb', echo=True)
metadata = orm.Base.metadata
metadata.create_all(engine) 
Session = sessionmaker(bind=engine)

g = geocoders.Google() 

def run():
  session = Session()
  
  try:
    while 1:
      rentals = session.query(Rental).filter(Rental.address != None).filter(Rental.lat == None).filter(Rental.lon == None)[:100]
      if not rentals: break
      
      for rental in rentals:
        try:
          place, (lat, lon) = list(g.geocode(rental.address, exactly_one=False))[0]
        except GQueryError:
          print "Query Error"
        else:
          rental.geom = WKTSpatialElement("POINT(%s %s)" % (lon, lat)
          print (place,lat,lon)
      print "Saving..."
      session.commit()
        
    while 1:
      sales = session.query(Sale).filter(Sale.address != None).filter(Sale.lat == None).filter(Sale.lon == None)[:100]
      if not sales: break
      for sale in sales:
        try:
          place, (lat, lon) = list(g.geocode(sale.address, exactly_one=False))[0]
        except GQueryError:
          print "Query Error"
        else:
          sale.geom = WKTSpatialElement("POINT(%s %s)" % (lon, lat)
          print (place,lat,lon)
      print "Saving..."
      session.commit()   
  except GTooManyQueriesError:
    session.commit()
    print "Reached Maximum Google Requests"

def help():
  print __doc__
  return 0
	
def process(arg='run'):
  if arg in _Functions:
    globals()[arg]()
	
class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
	  try:
		  opts, args = getopt.getopt(sys.argv[1:], "hl:d:", ["help","list=","database="])
	  except getopt.error, msg:
		  raise Usage(msg)
	
	  # process options
	  for o, a in opts:
		  if o in ("-h", "--help"):
			  for f in _Functions:
				  if f in args:
					  apply(f,(opts,args))
					  return 0
			  help()
	
	  # process arguments
	  for arg in args:
		  process(arg) # process() is defined elsewhere
  except Usage, err:
	  print >>sys.stderr, err.msg
	  print >>sys.stderr, "for help use --help"
	  return 2

if __name__ == "__main__":
  sys.exit(main())
