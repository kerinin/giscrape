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
  
  fig.suptitle("New Home Availability by Price", fontsize=18, weight='bold')
  session = Session()
    
  trim = int(session.query(Listing).count()/50.0)
  price_max = int( session.query(Listing).filter(Listing.price != None).order_by(-Listing.price)[trim].price )
  price_min = int( session.query(Listing).filter(Listing.price != None).order_by(Listing.price)[trim].price )
  step = int( (price_max-price_min)/100.0 )

  X = range(price_min, price_max, step)
  Y = array( [ session.query(Listing).filter(Listing.price >= x).filter(Listing.price < x+step).count() for x in X ], dtype=float )
  nY = array( [session.query(Listing).filter(Listing.price >= x).filter(Listing.price < x+step).filter(Listing.year_built >= 2009).count() for x in X ], dtype=float )
  C = array( [ session.query(Listing).filter(Listing.price < x).count() for x in X ], dtype=float )
  nC = array([ session.query(Listing).filter(Listing.price < x).filter(Listing.year_built >= 2009).count() for x in X ], dtype=float )
  
  ax.bar(X,100*nY / session.query(Listing).filter(Listing.year_built >= 2009).count(), width=step, color='g', edgecolor='g')
  ax.bar(X,100*Y / session.query(Listing).count(), width=step, color='k', linewidth=0, alpha=.3)
  ax.set_ylabel("Units Available (%)")
  ax.set_xlabel("Asking Price (Million $)")
  ax.axis([price_min,price_max,None,None])
  ax.xaxis.set_major_formatter(mFormatter)
  ax.axis([price_min,price_max,0,None])
  ax.grid(True)
  for line in ax.get_ygridlines():
    line.set_alpha(0)
  
  ax2 = ax.twinx()
  ax2.plot(X,100*C / session.query(Listing).count(),'k', alpha = .3, lw=2)
  ax2.plot(X,100*nC / session.query(Listing).filter(Listing.year_built >= 2009).count(),'k', lw=2)
  ax2.set_ylabel('Cumulative Units (%)')
  ax2.axis([price_min,price_max,0,100])
  ax2.xaxis.set_major_formatter(mFormatter)
  ax2.set_yticks(np.arange(0,101,10))
  ax.set_xticks(np.arange(0,price_max,250000))
  ax2.grid(True)
  
  ax.set_title("(All shown in grey)")
  if to_show:
    show()

if __name__ == "__main__":
  sys.exit(main())