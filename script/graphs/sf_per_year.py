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
  
  fig.suptitle("Residential Building Activity by Year", fontsize=18, weight='bold')
  s = Session()
  
  region = s.query(Context).get(4)
  q = s.query(TCADSegment).join(TCADSegment.improvement).filter(TCADImprovement.description.in_(['FOURPLEX','APARTMENT 100+','CONDO (STACKED)','APARTMENT 50-100', '1 FAM DWELLING', '2 FAM DWELLING', '1/2 DUPLEX', 'APARTMENT 5-25', 'APARTMENT 26-49']))

  X = range(1980, 2010)
  All = array( [ q.filter( TCADSegment.year_built == x ).value(func.sum(TCADSegment.area)) for x in X ], dtype=float )
  East = array( [ q.join(TCADImprovement.parcel).filter(TCAD_2010.the_geom.within(region.geom)).filter(TCADSegment.year_built == x).value(func.sum(TCADSegment.area)) for x in X ], dtype=float )
             
  ax = plt.subplot(111)
  p1=ax.bar(X,East/1e+6, width=.8, color='k', edgecolor='w', align='center')
  p2=ax.bar(X,(All-East)/1e+6, width=.8, color='.25', edgecolor='w', align='center', bottom=East/1e+6)
  
  ax.set_ylabel("Built Area (million sf)")
  ax.set_xlabel("Year")
  ax.grid(True)
  ax.axis([1980,2010,0,None])
  #ax.legend([p2,p1],['East Side', 'Austin'])
    
  show()

if __name__ == "__main__":
  sys.exit(main())
