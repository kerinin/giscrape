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
  
  fig.suptitle("Home Price/sf Distribution", fontsize=18, weight='bold')
  session = Session()

  per_sf_query = session.query(Listing).filter(Listing.price != None).filter(Listing.size != None).order_by(asc(Listing.price / Listing.size))
  trim = int( per_sf_query.count() * .01 )
  per_sf_min = int( per_sf_query.first().price / per_sf_query.first().size )
  per_sf_query = session.query(Listing).filter(Listing.price != None).filter(Listing.size != None).order_by(desc(Listing.price / Listing.size))
  per_sf_max = int( per_sf_query[trim].price / per_sf_query[trim].size )

  step = int( (per_sf_max-per_sf_min)/100.0 )

  X = arange(per_sf_min, per_sf_max, step)
  Y = [ per_sf_query.filter("listing.price / listing.size >= %s" % x).filter("listing.price / listing.size < %s" % (x + step)).count() for x in X ]
  C = [ per_sf_query.filter("listing.price / listing.size < %s" % (x + step)).count() for x in X ]
  
  ax.bar(X,Y, width=step, color='y', edgecolor='y')
  
  ax.set_ylabel("Units Available")
  ax.set_xlabel("Asking Price / sf ($/sf)")
  
  ax2 = ax.twinx()
  ax2.plot(X,C,'--k')
  ax2.set_ylabel('Cumulative Units')
  ax2.axis([per_sf_min,per_sf_max,None,None])
    
  show()

if __name__ == "__main__":
  sys.exit(main())