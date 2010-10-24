#! /usr/bin/env python
import sys, getopt, math, os, time
import locale
sys.path.append( os.path.dirname(sys.argv[0])+'/../../' )

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

import matplotlib as mpl
mpl.rcParams['font.size'] = 8

def main(argv=None):
  metadata.create_all()
  
  fig = plt.figure(figsize=(3,2.5))
  
  #fig.suptitle("Cost/SF Distribution by Distance", fontsize=18, weight='bold')
  shady = WKTSpatialElement("POINT(%s %s)" % (-97.699009500000003, 30.250421899999999) )
  session = Session()
  
  contexts = session.query(Context).order_by(Context.geom.area)
  boundary = session.query(Context).order_by(-Context.geom.area).first()
  #q = session.query(Listing).filter(Listing.contexts.any( id = boundary.id )).filter(Listing.geom != None).filter(Listing.price != None).filter(Listing.size != None)
  q = session.query(Listing).filter(Listing.geom.within(boundary.geom)).filter(Listing.geom != None).filter(Listing.price != None).filter(Listing.size != None)
  
  
  trim = int(q.count()/50.0)
  vmax = int( q.order_by(-Listing.price/Listing.size)[trim].price / q.order_by(-Listing.price/Listing.size)[trim].size)
  vmin = int( q.order_by(Listing.price/Listing.size).first().price / q.order_by(Listing.price/Listing.size).first().size )
  step = int( (vmax-vmin)/30.0 )
  
  X = arange(vmin, vmax, step)
  
  for i,context in enumerate( contexts.all() ):
    
    ax = plt.subplot(contexts.count(),1,i+1)
    
    #qi = q.filter(Listing.contexts.any( id = context.id ))
    qi = q.filter(Listing.geom.within(context.geom))
    
    Y = array( [ qi.filter("listing.price / listing.size >= %s" % x).filter("listing.price / listing.size < %s" % (x + step)).count() for x in X ], dtype=float)
    
    ax.bar(X,Y, width=step, color='k', edgecolor='w')

    ax.axis([vmin,vmax,0,None])
    ax.set_ylabel(context.name.replace(' ','\n'), rotation=0)
    ax.yaxis.set_major_formatter(NullFormatter())
    
    if not i+1 == contexts.count():
      ax.xaxis.set_major_formatter(NullFormatter())
    else:
      ax.set_xlabel('Asking Price / SF ($/sf)')
    
    ax.grid(True)

  plt.subplots_adjust(right=.95, top=.95, bottom=.15, left=.22)
  
  show()

if __name__ == "__main__":
  sys.exit(main())
