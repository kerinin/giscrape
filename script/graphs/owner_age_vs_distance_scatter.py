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
  
  boundary = session.query(Context).get(2)
  #q = session.query(Listing).filter(Listing.contexts.any( id = boundary.id )).filter(Listing.geom != None).filter(Listing.price != None).filter(Listing.size != None)
  q = session.query(TCAD_2010).join(TCAD_2010.person).filter(TCAD_2010.the_geom.within(boundary.geom))
  
  Ages = session.query(2010 - Person.birth_year).join(Person.owned_properties).filter(TCAD_2010.the_geom.within(boundary.geom)).order_by(TCAD_2010.objectid).all()
  Values = session.query(TCAD_2010.market_value).join(TCAD_2010.person).filter(TCAD_2010.the_geom.within(boundary.geom)).order_by(TCAD_2010.objectid).all()

  prop = session.query(TCAD_2010).join(TCAD_2010.person).filter(TCAD_2010.the_geom.within(boundary.geom)).order_by(TCAD_2010.objectid).first()
  print prop.market_value
  print Values[0]
  
  print 2010 - prop.person.birth_year
  print Ages[0]
  
  ax = plt.subplot(111)
  ax.plot(Ages, Values, 'k,')

  ax.axis([20,100,None,500000])
  ax.set_ylabel("Property Value ($)")
  ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos: "%sk" % str(int(x/1000))))
  
  ax.set_xlabel('Age')
  
  ax.grid(True)

  plt.subplots_adjust(right=.95, top=.95, bottom=.15, left=.22)
  
  show()

if __name__ == "__main__":
  sys.exit(main())
