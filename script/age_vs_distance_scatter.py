#! /usr/bin/env python

import sys, getopt, math, datetime, os
import locale

from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql.expression import *
import geoalchemy
from geoalchemy import *

from numpy import *
from pylab import *
from matplotlib.ticker import *
from matplotlib.scale import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from unum.units import *

from giscrape import orm
from giscrape.orm import *

def main(argv=None):

  fig = plt.figure()
  
  fig.suptitle("Age vs Distance", fontsize=18, weight='bold')
  shady = WKTSpatialElement("POINT(%s %s)" % (-97.699009500000003, 30.250421899999999) )
  session = Session()
  q = session.query(Listing).filter(Listing.geom != None).filter(Listing.year_built != None).filter(Listing.geom.transform(32139).distance(shady.transform(32139)) < (2.5 * mile).asNumber(m) ).order_by(-Listing.year_built)
  
  X = [ (session.scalar(x.geom.transform(32139).distance(shady.transform(32139))) * m ).asNumber(mile) for x in q[:-5] ]
  Y = [ x.year_built for x in q[:-5] ]
  
  ax = plt.subplot(111)
  ax.plot(X,Y,'om')
  ax.grid(True)
  ax.set_ylabel("Year Built")
  ax.set_xlabel("Distance from Site (miles)")
  
  show()
  
if __name__ == "__main__":
  sys.exit(main())