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
  
  fig.suptitle("Cost Distribution by Distance", fontsize=18, weight='bold')
  shady = WKTSpatialElement("POINT(%s %s)" % (-97.699009500000003, 30.250421899999999) )
  session = Session()
  
  contexts = session.query(Context).order_by(Context.geom.area)
  boundary = session.query(Context).order_by(-Context.geom.area).first()
  q = session.query(Listing).filter(Listing.contexts.any( id = boundary.id )).filter(Listing.geom != None).filter(Listing.price != None)
  
  trim = int(q.count()/50.0)
  price_max = int( q.order_by(-Listing.price)[trim].price )
  price_min = int( q.order_by(Listing.price).first().price )
  step = int( (price_max-price_min)/30.0 )
  
  X = range(price_min, price_max, step)
  
  for i,context in enumerate( contexts.all() ):
    
    ax = plt.subplot(contexts.count(),1,i+1)
    
    qi = q.filter(Listing.contexts.any( id = context.id ))
    
    Y = array( [ qi.filter(Listing.price >= x).filter(Listing.price < x+step).count() for x in X ], dtype=float )
    
    ax.bar(X,Y, width=step, color='g', edgecolor='g')

    ax.axis([price_min,price_max,0,None])
    ax.set_xticks(np.arange(0,price_max,50000))
    ax.set_ylabel(context.name.replace(' ','\n'), rotation=0)
    
    if not i+1 == contexts.count():
      ax.xaxis.set_major_formatter(NullFormatter())
    else:
      ax.xaxis.set_major_formatter(mFormatter)
      ax.set_xlabel('Asking Price ($)')
    
    ax.grid(True)
    
  show()


if __name__ == "__main__":
  sys.exit(main())