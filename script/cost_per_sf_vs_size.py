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
  
  fig.suptitle("Cost/SF vs Size", fontsize=18, weight='bold')
  shady = WKTSpatialElement("POINT(%s %s)" % (-97.699009500000003, 30.250421899999999) )
  session = Session()
  q = session.query(Listing).filter(Listing.geom != None).filter(Listing.price != None).filter(Listing.size != None)
  
  context = q.filter(Listing.geom.transform(32139).distance(shady.transform(32139)) < (2.5 * mile).asNumber(m) ).order_by(-Listing.geom.transform(32139).distance(shady.transform(32139)))

  X = [ x.price / x.size for x in context.all() ]
  Y = [ x.size for x in context ]
  S = 20*array( [ (session.scalar(x.geom.transform(32139).distance(shady.transform(32139))) * m ).asNumber(mile) for x in context ], dtype=float )**3
  
  ax = plt.subplot(111)
  
  ax.scatter(X,Y,S,'c', alpha=.75)
  
  ax.set_title('Dot size denotes distance from site')
  ax.set_xlabel('Asking Price / SF ($/sf)')
  ax.set_ylabel('Size (sf)')
    
  ax.grid(True)
  ax.axis([0,400,500,2000])

  show()

if __name__ == "__main__":
  sys.exit(main())