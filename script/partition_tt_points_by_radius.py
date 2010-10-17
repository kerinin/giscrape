#! /usr/bin/env python

import sys, getopt, math, os, time
import locale
sys.path.append( os.path.dirname(sys.argv[0])+'/../' )



from giscrape.orm import *

def main(argv=None):
  shady = WKTSpatialElement("POINT(%s %s)" % (-97.699009500000003, 30.250421899999999) )
  s=Session()
  import time
  
  q = s.query(TravelTimePoint).filter('gis_schema.travel_distance.radius_5000 IS NULL').order_by(-TravelTimePoint.speed_limit)

  #point_base = s.query(TravelTimePoint).order_by(TravelTimePoint.speed_limit).first()
  #q = s.query(TravelTimePoint).filter(TravelTimePoint.redundant_checked == False).order_by(TravelTimePoint.geom.distance(point_base.geom))

  while q.count():
    for p in q[:100]:
      point = s.query(TravelTimePoint).get(p.id)
      #if point.radius_100 == None:
      #  print "Point %s" % point.id
      #  s.query(TravelTimePoint).filter(TravelTimePoint.id != p.id).filter(TravelTimePoint.geom.within_distance(p.geom, 100)).update({"radius_100" : False}, synchronize_session=False)
      #  point.radius_100 = True
      #if point.radius_1000 == None:
      #  print "Point %s" % point.id
      #  s.query(TravelTimePoint).filter(TravelTimePoint.id != p.id).filter(TravelTimePoint.geom.within_distance(p.geom, 1000)).update({"radius_1000" : False}, synchronize_session=False)
      #  point.radius_1000 = True
      if point.radius_5000 == None:
        print "Point %s" % point.id
        s.query(TravelTimePoint).filter(TravelTimePoint.id != p.id).filter(TravelTimePoint.geom.within_distance(p.geom, 5000)).update({"radius_5000" : False}, synchronize_session=False)
        point.radius_5000 = True
        
      s.merge(point)
    print "Committing..."
    #print "Radius 100 - True: %s, False: %s, NULL: %s" % (
    #  s.query(TravelTimePoint).filter('gis_schema.travel_distance.radius_100 = TRUE').count(),
    #  s.query(TravelTimePoint).filter('gis_schema.travel_distance.radius_100 = FALSE').count(),
    #  s.query(TravelTimePoint).filter('gis_schema.travel_distance.radius_100 IS NULL').count()
    #)
    #print "Radius 1000 - True: %s, False: %s, NULL: %s" % (
    #  s.query(TravelTimePoint).filter('gis_schema.travel_distance.radius_1000 = TRUE').count(),
    #  s.query(TravelTimePoint).filter('gis_schema.travel_distance.radius_1000 = FALSE').count(),
    #  s.query(TravelTimePoint).filter('gis_schema.travel_distance.radius_1000 IS NULL').count()
    #)
    print "Radius 5000 - True: %s, False: %s, NULL: %s" % (
      s.query(TravelTimePoint).filter('gis_schema.travel_distance.radius_5000 = TRUE').count(),
      s.query(TravelTimePoint).filter('gis_schema.travel_distance.radius_5000 = FALSE').count(),
      s.query(TravelTimePoint).filter('gis_schema.travel_distance.radius_5000 IS NULL').count()
    )
    s.commit()
  

if __name__ == "__main__":
  sys.exit(main())
