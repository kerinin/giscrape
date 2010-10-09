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

g = geocoders.Google() 
#g = geocoders.Yahoo('njjoUkPV34EK.D.t1Ev79ZEFAZtrCdSxDqGdlsNUPVQahXlcWxWTellv1bvHDA--')
#g = geocoders.GeocoderDotUS()  

def run():
  session = Session()
  
  try:
    while 1:
      rentals = session.query(Rental).filter(Rental.address != None).filter(Rental.lat == None).filter(Rental.lon == None)[:100]
      if not rentals: break
      for rental in rentals:
        try:
          place, (lat, lon) = list(g.geocode(rental.address, exactly_one=False))[0]
        except GQueryError as (error, text):
          print "Query Error"
          print error
          print text
        else:
          rental.geom = WKTSpatialElement("POINT(%s %s)" % (lon, lat) )
          rental.lat = lat
          rental.lon = lon
          print (place,lat,lon)
      print "Saving..."
      session.commit()
        
    while 1:
      sales = session.query(Sale).filter(Sale.address != None).filter(Sale.lat == None).filter(Sale.lon == None)[:100]
      if not sales: break
      for sale in sales:
        try:
          place, (lat, lon) = list(g.geocode(sale.address, exactly_one=False))[0]
        except GQueryError as error:
          print "Query Error"
          print error
          print sale.address
          sale.lat = 0
          sale.lon = 0
        else:
          sale.geom = WKTSpatialElement("POINT(%s %s)" % (lon, lat) )
          sale.lat = lat
          sale.lon = lon
          print (place,lat,lon)
        
      print "Saving..."
      session.commit()   
      
    while 1:
      listings = session.query(Listing).filter(Listing.address != None).filter(Listing.lat == None).filter(Listing.lon == None)[:100]
      if not listings: break
      for listing in listings:
        try:
          place, (lat, lon) = list(g.geocode(listing.address, exactly_one=False))[0]
        except GQueryError as error:
          print "Query Error"
          print error
          print listing.address
          listing.lat = 0
          listing.lon = 0
        else:
          listing.geom = WKTSpatialElement("POINT(%s %s)" % (lon, lat) )
          listing.lat = lat
          listing.lon = lon
          print (place,lat,lon)
        
      print "Saving..."
      session.commit()   
  except GTooManyQueriesError:
    session.commit()
    print "Reached Maximum Google Requests"
    
  
  print "Finding enclosing TCAD Parcels"
  for listing in session.query(Listing).filter(Listing.tcad_2008_id == None).filter(Listing.geom != None).all():
    q = session.query(TCAD_2008).filter(TCAD_2008.the_geom.covers(listing.geom.transform(2277)))
    if q.count():
      listing.tcad_2008_parcel = q.first()
      print "$%s / $%s (%s)" % (listing.tcad_2008_parcel.marketvalu, listing.price, listing.address)
  session.commit()

  for sale in session.query(Sale).filter(Sale.tcad_2008_id == None).filter(Sale.geom != None).all():
    q = session.query(TCAD_2008).filter(TCAD_2008.the_geom.covers(sale.geom.transform(2277)))
    if q.count():
      sale.tcad_2008_parcel = q.first()
      print "$%s / $%s (%s)" % (sale.tcad_2008_parcel.marketvalu, sale.price, sale.address)
  session.commit()
  
  for rental in session.query(Rental).filter(Rental.tcad_2008_id == None).filter(Rental.geom != None).all():
    q = session.query(TCAD_2008).filter(TCAD_2008.the_geom.covers(rental.geom.transform(2277)))
    if q.count():
      rental.tcad_2008_parcel = q.first()
      print "$%s / $%s (%s)" % (rental.tcad_2008_parcel.marketvalu, rental.price, rental.address)
  session.commit()


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
