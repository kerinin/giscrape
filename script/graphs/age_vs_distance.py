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
  q = session.query(TCAD_2010).join(TCAD_2010.person).filter(TCAD_2010.the_geom.within(boundary.geom))
  
  segments = [[20,30], [30,40], [40,50], [50,60], [60,70], [70,80], [80,90], [90,100]]
  
  X = [ x[0] for x in segments ]
  Width = [ x[1]-x[0] for x in segments ]
  
  for i,context in enumerate( contexts.all() ):
    
    ax = plt.subplot(contexts.count(),1,i+1)
    
    qi = q.filter(TCAD_2010.the_geom.within(context.geom))
    
    Y = array( [ qi.filter(Person.birth_year <= 2010 - x[0]).filter(Person.birth_year > 2010 - x[1]).count() for x in segments ], dtype=float)
    
    ax.bar(X,Y, width=Width, color='k', edgecolor='w')

    ax.axis([20,100,0,None])
    ax.set_ylabel(context.name.replace(' ','\n'), rotation=0)
    ax.yaxis.set_major_formatter(NullFormatter())
    
    if not i+1 == contexts.count():
      ax.xaxis.set_major_formatter(NullFormatter())
    else:
      ax.set_xlabel('Age')
    
    ax.grid(True)

  plt.subplots_adjust(right=.95, top=.95, bottom=.15, left=.22)
  
  show()

if __name__ == "__main__":
  sys.exit(main())
