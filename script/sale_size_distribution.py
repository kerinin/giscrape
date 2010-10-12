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
  
  fig.suptitle("Home Size Distribution", fontsize=18, weight='bold')
  
  session = Session()
  
  area_query = session.query(Listing).filter(Listing.size != None)
  total = area_query.count()
  trim = int( total * .02 )
  max_area = area_query.order_by(desc(Listing.size))[trim].size
  min_area = area_query.order_by(asc(Listing.size)).first().size
  step = int( (max_area - min_area)/100.0 )
  
  X = arange(min_area, max_area, step)
  Y = [ area_query.filter("listing.size >= %s" % str(x)).filter("listing.size < %s" % str(x+step)).count() for x in X ]
  C = [ 100*float(area_query.filter("listing.size < %s" % str(x+step)).count())/total for x in X ]
  
  ax.bar(X,Y, width=step, color='c',edgecolor='c')
  
  ax.set_ylabel("Units Available")
  ax.set_xlabel("Size (sf)")
  
  ax2 = ax.twinx()
  ax2.plot(X,C,'--k')
  ax2.set_ylabel('Cumulative Units (%)')
  ax2.axis([min_area,max_area,None,None])
  
  show()

if __name__ == "__main__":
  sys.exit(main())