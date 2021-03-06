#! /usr/bin/env python

import sys, getopt, math, os, time
import locale
sys.path.append( os.path.dirname(sys.argv[0])+'/../' )

from giscrape.orm import *
from google.directions import GoogleDirections

travel_type = None
lat = None
lon = None

from giscrape.googlemaps import *
gmaps = GoogleMaps()

def help():
  print "python travel_distance.py [all|driving|bicycling|walking] --lat=<latitude> --lon=<longitude>"
  print __doc__
  return 0
	
class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(sys.argv[1:], "h", ["help","lat=","lon="])
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

    metadata.create_all()

    LAT = '30.250421899999999'
    LON = '-97.699009500000003'
    ORIGIN = "Shady Lane"
    MODE = "driving"
    RADIUS = TravelTimePoint.radius_1000
    ORIGIN_POINT = WKTSpatialElement("POINT(%s %s)" % (LON, LAT) )
    
    s=Session()
    q=s.query(TravelTimePoint).filter(RADIUS == True).filter( not_( TravelTimePoint.times.any( and_( TravelTime.origin==ORIGIN, TravelTime.mode==MODE) ) ) ).order_by(TravelTimePoint.geom.distance(ORIGIN_POINT.transform(2277)))
    try:
      while q.count():
        for destination in q[:100]:
          try:
            s.query(TravelTime).filter(TravelTime.origin==ORIGIN).filter(TravelTime.mode==MODE).filter(TravelTime.destination_id == destination.id).delete()

            dlat = s.scalar(destination.geom.transform(4326).y)
            dlon = s.scalar(destination.geom.transform(4326).x)
            directions = gmaps.directions('%s,%s' % (LAT, LON),'%s,%s' % (dlat,dlon), mode=MODE)

            time = TravelTime( 
              origin=ORIGIN, 
              destination = destination, 
              mode=MODE, 
              duration = int(directions['routes'][0]['legs'][0]['duration']['value'])/60
            )
            
            s.add(time)

            print "Dest: %s, %s, duration: %s minutes" % (dlat, dlon, time.duration)
            for t in destination.times:
              print t.id
          except GoogleMapsError as err:
            if "ZERO_RESULTS" in err:
              print "zero results..."
            else:
              raise
          
        s.commit()
        print "Committed... %s remaining" % q.count()
    except GoogleMapsError as err:
      s.commit()
      print "Reached max requests and committed (%s)" % err
      
  except Usage, err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

if __name__ == "__main__":
  sys.exit(main())
