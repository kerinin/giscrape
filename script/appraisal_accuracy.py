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
  
  fig.suptitle("Ratio Distribution of Asking Price to TCAD Appraisal", fontsize=18, weight='bold')
  session = Session()
  
  q = session.query(Listing).join(TCAD_2008).filter(TCAD_2008.marketvalu > 1000).filter(Listing.price > 1000)
  
  X = [ x.price / ( x.tcad_2008_parcel.marketvalu )  for x in q.all() ]
  Y = [ x.price for x in q.all() ]
  
  ax = plt.subplot(111)
  ax.hist(X,200,(0,2.5), color='g', edgecolor='g')
  ax.grid(True)
  for line in ax.get_ygridlines():
    line.set_alpha(0)

  ax2 = ax.twinx() 
  ax2.hist(X,1000,(0,10), normed=True, histtype='step', cumulative=True, color='k')
  ax2.grid(True)
  ax2.axis([0,2.5,0,1])
  #ax.set_xticks(np.arange(0,5,.5))
  ax2.set_yticks(np.arange(0,1,.1))
  #ax2.yaxis.set_major_formatter(mFormatter)
  #ax2.xaxis.set_major_formatter(yFormatter)
  
  show()

if __name__ == "__main__":
  sys.exit(main())