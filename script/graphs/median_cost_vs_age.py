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
  
  fig.suptitle("Asking Price Distribution by Age", fontsize=18, weight='bold')
  
  session = Session()
  
  q = session.query(Listing).filter(Listing.year_built != None).filter(Listing.price != None)
  total = q.count()
  trim = int( total * .01 )
  first_date = q.order_by(asc(Listing.year_built))[trim].year_built
  last_date = q.order_by(desc(Listing.year_built)).first().year_built
  step = int((last_date - first_date)/12. )
  
  def prices(start,end):
    return [ x.price for x in q.filter('listing.year_built >= %s' % start).filter('listing.year_built < %s' % end).all() ]
    
  X = arange(first_date, last_date, step)
  Y = [ prices(x,x+step) for x in X ]
  C = [ len(y) for y in Y ]
  

  ax.set_title("Boxes show median and quartiles, lines show inner quartile range")   
  ax.set_xlabel("Year Built")
  p1=ax.plot(X,C,'--k', alpha=.5, zorder=-1)
  ax.set_ylabel('Sample Size')
  
  ax2 = ax.twinx() 
  ax2.boxplot(Y, sym='', whis=1.5, positions=X, widths=(.5*step))
  ax2.set_ylabel("Asking Price Distribution ($)")
  ax2.grid(True)
  ax2.axis([first_date-(step/2),last_date,None,None])
  ax2.yaxis.set_major_formatter(mFormatter)
  ax2.xaxis.set_major_formatter(yFormatter)
  
  legend([p1],['Sample Size'], loc=2)
  show()

if __name__ == "__main__":
  sys.exit(main())