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
  
  # Properties which have no segments built after 2000
  q = session.query(TCAD_2010).filter(not_( TCAD_2010.improvements.any(TCADImprovement.segments.any(TCADSegment.year_built > 2000 ) ) ) ).filter(TCAD_2010.prop_id > 0 ).filter(TCAD_2010.the_geom.within(boundary.geom))

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
  

if __name__ == "__main__":
  sys.exit(main())
