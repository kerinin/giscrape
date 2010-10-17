#! /usr/bin/env python

import sys, getopt, math, os, time
import locale
sys.path.append( os.path.dirname(sys.argv[0])+'/../' )



from giscrape.orm import *

def main(argv=None):
  shady = WKTSpatialElement("POINT(%s %s)" % (-97.699009500000003, 30.250421899999999) )
  s=Session()
  import time
  
  q = s.query(TravelTimePoint).filter(TravelTimePoint.redundant_checked == False).order_by(-TravelTimePoint.speed_limit)

  #point_base = s.query(TravelTimePoint).order_by(TravelTimePoint.speed_limit).first()
  #q = s.query(TravelTimePoint).filter(TravelTimePoint.redundant_checked == False).order_by(TravelTimePoint.geom.distance(point_base.geom))

  while q.count():
    for p in q[:1000]:
      point = s.query(TravelTimePoint).get(p.id)
      if point:
        print "Point %s" % point.id
        s.query(TravelTimePoint).filter(TravelTimePoint.id != p.id).filter(TravelTimePoint.geom.within_distance(p.geom, 50)).delete(synchronize_session='fetch')
        point.redundant_checked = True
        s.merge(point)
    print "Committing..."
    print "%s remaining, %s total" % (q.count(), s.query(TravelTimePoint).count())
    s.commit()
  

if __name__ == "__main__":
  sys.exit(main())
