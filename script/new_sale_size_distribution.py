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
  
  fig.suptitle("New Home Size Distribution", fontsize=18, weight='bold')
  
  session = Session()
  
  area_query = session.query(Listing).filter(Listing.size != None)
  total = area_query.count()
  trim = int( total * .02 )
  max_area = area_query.order_by(desc(Listing.size))[trim].size
  min_area = area_query.order_by(asc(Listing.size)).first().size
  step = int( (max_area - min_area)/100.0 )
  
  X = arange(min_area, max_area, step)
  Y = array( [ area_query.filter("listing.size >= %s" % str(x)).filter("listing.size < %s" % str(x+step)).count() for x in X ], dtype=float )
  C = array( [ area_query.filter("listing.size < %s" % x).count() for x in X], dtype = float )
  nY = array( [ area_query.filter("listing.size >= %s" % str(x)).filter("listing.size < %s" % str(x+step)).filter(Listing.year_built >= 2009).count() for x in X ], dtype=float )
  nC = array( [ area_query.filter("listing.size < %s" % x).filter(Listing.year_built >= 2009).count() for x in X], dtype = float )
  
  ax.bar(X,100*nY/area_query.filter(Listing.year_built >= 2009).count(), width=step, color='c',edgecolor='c')
  ax.bar(X,100*Y/area_query.count(), width=step, color='k', linewidth=0, alpha=.3)
  ax.set_ylabel("Units Available (%)")
  ax.set_xlabel("Size (sf)")
  ax.axis([min_area,max_area,0,None])
  ax.grid(True)
  for line in ax.get_ygridlines():
    line.set_alpha(0)
      
  ax2 = ax.twinx()
  ax2.plot(X,100*C/area_query.count(),'k', alpha=.3, lw=2)
  ax2.plot(X,100*nC/area_query.filter(Listing.year_built >= 2009).count(),'k', lw=2)
  ax2.set_ylabel('Cumulative Units (%)')
  ax2.axis([min_area,max_area,0,100])
  ax2.set_yticks(np.arange(0,101,10))
  ax.set_xticks(np.arange(0,max_area,500))
  ax2.grid(True)
  
  ax.set_title("(All shown in grey)")
  show()

if __name__ == "__main__":
  sys.exit(main())