#! /usr/bin/env python

import sys, getopt, math, os, time
import locale
sys.path.append( os.path.dirname(sys.argv[0])+'/../../' )

from sqlalchemy import create_engine, func
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

  fig = plt.figure(figsize=(3,2.5))
  
  #fig.suptitle("Residential Growth by Year", fontsize=18, weight='bold')
  s = Session()
  
  region = s.query(Context).get(3)
  q = s.query(TCADSegment).join(TCADSegment.improvement).filter(TCADImprovement.description.in_(['FOURPLEX','APARTMENT 100+','CONDO (STACKED)','APARTMENT 50-100', '1 FAM DWELLING', '2 FAM DWELLING', '1/2 DUPLEX', 'APARTMENT 5-25', 'APARTMENT 26-49']))

  X = range(1980, 2010)
  All = array( [ q.filter( TCADSegment.year_built == x ).value(func.sum(TCADSegment.area)) for x in X ], dtype=float )
  All_norm = array( [ q.filter( TCADSegment.year_built <= x ).value(func.sum(TCADSegment.area)) for x in X ], dtype=float )
  East = array( [ q.join(TCADImprovement.parcel).filter(TCAD_2010.the_geom.within(region.geom)).filter(TCADSegment.year_built == x).value(func.sum(TCADSegment.area)) for x in X ], dtype=float )
  East_norm = array( [ q.join(TCADImprovement.parcel).filter(TCAD_2010.the_geom.within(region.geom)).filter(TCADSegment.year_built <= x).value(func.sum(TCADSegment.area)) for x in X ], dtype=float )
             
  ax = plt.subplot(111)
  p2=ax.plot(X,100 * All/All_norm, color='.75')
  p1=ax.plot(X,100 * East/East_norm, color='k', lw=2)
  
  
  ax.set_ylabel("Growth in Square Feet (%)")
  ax.set_xlabel("Year")
  ax.grid(True)
  ax.axis([1980,2010,0,5])
  ax.legend([p2,p1],['All Austin','East Side'], loc='upper left')
    
  plt.subplots_adjust(right=.93, top=.95, bottom=.15, left=.15)
  
  show()

if __name__ == "__main__":
  sys.exit(main())
