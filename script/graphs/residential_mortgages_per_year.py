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

def main(argv=None):

  fig = plt.figure()
  
  fig.suptitle("Mortgages Since 2000", fontsize=18, weight='bold')
  s = Session()
  
  region = s.query(Context).get(3)
  q = s.query(TCADValueHistory).join(TCADValueHistory.parcel).join(TCAD_2010.improvements).join(TCADImprovement.segments).filter(TCADImprovement.description == '1 FAM DWELLING')

  step = 50000
  
  X = range(2000, 2009)
  MAmount = range(0,500000, step)

  labels = list()
  CCs = list()
  Plots = list()
  
  for value_min in MAmount:
    value_max = value_min + step
    All = array( [ q.filter(TCADValueHistory.value >= value_min).filter(TCADValueHistory.value < value_max).filter(TCADValueHistory.year == x + 1).filter(TCADSegment.year_built == x).filter(not_(TCAD_2010.improvements.any(TCADImprovement.segments.any( TCADSegment.year_built < x)))).count() for x in X ], dtype=float )
    East = array( [ q.filter(TCADValueHistory.value >= value_min).filter(TCADValueHistory.value < value_max).filter(TCADValueHistory.year == x + 1).filter(TCADSegment.year_built == x).filter(not_(TCAD_2010.improvements.any(TCADImprovement.segments.any( TCADSegment.year_built < x)))).filter(TCAD_2010.the_geom.within(region.geom)).count() for x in X ], dtype=float )

    CCs.append(corrcoef(East, All)[0,1])
    Plots.append( [All, East, value_min, value_max] )
    
    print value_min
    
  for i, values in enumerate(Plots):
    if i % 2:
      count = len(MAmount)/2
      All = values[0]+Plots[i-1][0]
      East = values[1]+Plots[i-1][1]
      
      top = plt.subplot( 3,count, 1 + count + (i/2))
      bottom = plt.subplot( 3,count, 1 + 2*count + (i/2))
      top.plot(X,East, lw=2, color='k')
      bottom.plot(X,All, lw=1, color='k', ls='--')
      
      top.set_title("$%sk-$%sk" % (Plots[i-1][2]/1000, values[3]/1000))
      
      top.xaxis.set_major_formatter( NullFormatter() )
      top.yaxis.set_major_formatter( NullFormatter() )
      top.xaxis.set_major_locator( NullLocator() )
      top.yaxis.set_major_locator( NullLocator() )
      bottom.xaxis.set_major_formatter( NullFormatter() )
      bottom.yaxis.set_major_formatter( NullFormatter() )
      bottom.xaxis.set_major_locator( NullLocator() )
      bottom.yaxis.set_major_locator( NullLocator() )    
      
      if i == 0:
        top.set_ylabel("East Side")
        bottom.set_ylabel("Austin")
  
  corr = plt.subplot(3,1,1)
  p1=corr.plot(MAmount, CCs, lw=2, color='k')
  corr.axhline(color='k')
  
  #p2=ax.plot(X,All, ls="--", label=("East Side $%s - $%s" % (value_min, value_max)))
  corr.hspace = .5
  corr.xaxis.set_major_formatter( ticker.FuncFormatter(lambda x,pos: str(int(x/1000.0))+'k' ) )
  corr.set_ylabel("Correlation Coefficient")
  #corr.set_xlabel("Mortgage Amount ($)")
  corr.grid(True)
  corr.axis([None,None,-1,1])
    
  #ax.legend()
    
  show()

if __name__ == "__main__":
  sys.exit(main())
