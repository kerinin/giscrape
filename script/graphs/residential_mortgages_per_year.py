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

  fig = plt.figure(figsize=(6,4))
  
  #fig.suptitle("Mortgages Since 2000", fontsize=18, weight='bold')
  s = Session()
  
  region = s.query(Context).get(3)
  q = s.query(TCADValueHistory).join(TCADValueHistory.parcel).join(TCAD_2010.improvements).join(TCADImprovement.segments).filter(TCADImprovement.description == '1 FAM DWELLING')

  step = 50000
  
  X = range(2000, 2009)
  MAmount = range(0,500000, step)

  labels = list()
  CCs = list()
  Plots = list()
  
  All_low = array( [ q.filter(TCADValueHistory.value < 225000).filter(TCADValueHistory.year == x + 1).filter(TCADSegment.year_built == x).filter(not_(TCAD_2010.improvements.any(TCADImprovement.segments.any( TCADSegment.year_built < x)))).count() for x in X ], dtype=float )
  All_high = array( [ q.filter(TCADValueHistory.value >= 225000).filter(TCADValueHistory.year == x + 1).filter(TCADSegment.year_built == x).filter(not_(TCAD_2010.improvements.any(TCADImprovement.segments.any( TCADSegment.year_built < x)))).count() for x in X ], dtype=float )
  East_low = array( [ q.filter(TCADValueHistory.value < 225000).filter(TCADValueHistory.year == x + 1).filter(TCADSegment.year_built == x).filter(not_(TCAD_2010.improvements.any(TCADImprovement.segments.any( TCADSegment.year_built < x)))).filter(TCAD_2010.the_geom.within(region.geom)).count() for x in X ], dtype=float )
  East_high = array( [ q.filter(TCADValueHistory.value >= 225000).filter(TCADValueHistory.year == x + 1).filter(TCADSegment.year_built == x).filter(not_(TCAD_2010.improvements.any(TCADImprovement.segments.any( TCADSegment.year_built < x)))).filter(TCAD_2010.the_geom.within(region.geom)).count() for x in X ], dtype=float )
    
  CClow = corrcoef(All_low, East_low)[0,1]
  CChigh = corrcoef(All_high, East_high)[0,1]
  
  tl = plt.subplot(2,2,1)
  tl.plot(X, All_low, color='.75')
  plt.subplots_adjust(right=.99, top=.99, bottom=.15, left=.15)
  
  tl.set_ylabel("New Houses (All Austin)")
  plt.grid(True)
  plt.subplots_adjust(right=.99, top=.99, bottom=.15, left=.15)
  
  tr = plt.subplot(2,2,2, sharey=tl)
  tr.plot(X, All_high, color='.75')
  plt.grid(True)
  plt.subplots_adjust(right=.99, top=.99, bottom=.15, left=.15)
  
  bl = plt.subplot(2,2,3, sharex=tl)
  bl.plot(X, East_low, color='k', lw=2)
  bl.set_ylabel("New Houses (East Side)")
  bl.set_xlabel("Appraised Value < $225k\nCorrelation Coef: %.2f" % CClow)
  plt.grid(True)
  plt.subplots_adjust(right=.99, top=.99, bottom=.15, left=.15)
  
  br = plt.subplot(2,2,4, sharey=bl, sharex=tr)
  br.plot(X, East_high, color='k', lw=2)
  br.set_xlabel("Appraised Value > $225k\nCorrelation Coef: %.2f" % CChigh)
  plt.grid(True)
  plt.subplots_adjust(right=.99, top=.99, bottom=.15, left=.15)
  
  bl.xaxis.set_major_formatter(FuncFormatter(lambda x,pos: "'%s" % str(int(x)+1)[-2:] ))
  br.xaxis.set_major_formatter(FuncFormatter(lambda x,pos: "'%s" % str(int(x)+1)[-2:] ))
  
  ticklabels = tl.get_xticklabels()+tr.get_xticklabels()+tr.get_yticklabels()+br.get_yticklabels()
  setp(ticklabels, visible=False)   

  plt.subplots_adjust(right=.96, top=.96, bottom=.15, left=.15)
   
  show()

if __name__ == "__main__":
  sys.exit(main())
