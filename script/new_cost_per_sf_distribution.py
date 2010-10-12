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
  
  fig.suptitle("New Home Price/sf Distribution", fontsize=18, weight='bold')
  session = Session()

  per_sf_query = session.query(Listing).filter(Listing.price != None).filter(Listing.size != None).order_by(asc(Listing.price / Listing.size))
  trim = int( per_sf_query.count() * .01 )
  per_sf_min = int( per_sf_query.first().price / per_sf_query.first().size )
  per_sf_query = session.query(Listing).filter(Listing.price != None).filter(Listing.size != None).order_by(desc(Listing.price / Listing.size))
  per_sf_max = int( per_sf_query[trim].price / per_sf_query[trim].size )

  step = int( (per_sf_max-per_sf_min)/100.0 )

  X = arange(per_sf_min, per_sf_max, step)
  Y = array( [ per_sf_query.filter("listing.price / listing.size >= %s" % x).filter("listing.price / listing.size < %s" % (x + step)).count() for x in X ], dtype=float)
  nY = array( [ per_sf_query.filter("listing.price / listing.size >= %s" % x).filter("listing.price / listing.size < %s" % (x + step)).filter(Listing.year_built >= 2009).count() for x in X ], dtype=float)
  C = array( [ per_sf_query.filter("listing.price / listing.size < %s" % (x + step)).count() for x in X ], dtype=float)
  nC = array( [ per_sf_query.filter("listing.price / listing.size < %s" % (x + step)).filter(Listing.year_built >= 2009).count() for x in X ], dtype=float)
  
  ax.bar(X,100 * nY / per_sf_query.filter(Listing.year_built >= 2009).count(), width=step, color='y', edgecolor='y')
  ax.bar(X,100 * Y / per_sf_query.count(), width=step, color='k', linewidth=0, alpha=.3)
  ax.set_ylabel("Units Available (%)")
  ax.set_xlabel("Asking Price / sf ($/sf)")
  ax.axis([per_sf_min,per_sf_max,0,None])
  ax.grid(True)
  for line in ax.get_ygridlines():
    line.set_alpha(0)
     
  ax2 = ax.twinx()
  ax2.plot(X,100*C/per_sf_query.count(),'k', alpha=.3, lw=2)
  ax2.plot(X,100*nC/per_sf_query.filter(Listing.year_built >= 2009).count(),'k', lw=2)
  ax2.set_ylabel('Cumulative Units (%)')
  ax2.axis([per_sf_min,per_sf_max,0,100])
  ax2.set_yticks(np.arange(0,101,10))
  ax.set_xticks(np.arange(0,per_sf_max,50))
  ax2.grid(True)
    
  ax.set_title("(All shown in grey)")
  show()

if __name__ == "__main__":
  sys.exit(main())