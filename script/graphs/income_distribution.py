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

  fig = plt.figure(figsize=(6,2))
  
  start_austin = array( [0,10000,15000,25000,35000,50000,75000,100000,150000,200000], dtype = int )
  width_austin = array( [10000, 5000,10000, 10000, 15000, 25000,25000,50000, 50000, 50000])
  austin_count = array( [24865,14124,30868,34260,44379,54995,33999,35134,14859,15872], dtype=int )
  
  start_usa = array( [0, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 60000, 75000, 100000, 125000, 150000, 200000], dtype=int )
  width_usa = array( [10000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 10000, 15000, 25000, 25000, 25000, 50000, 50000], dtype=int )
  usa_count = array( [ 8045626, 6139558, 5951218, 5969858, 5921704, 5977646, 5521646, 5549466, 4880035, 9398215, 11711656, 13992314, 8736798, 5021306, 4858631, 4710621 ], dtype=float )
  
  l = plt.subplot(2,1,1)
  plt.grid(True)
  l.bar(start_usa, usa_count, width=width_usa, color='.75', edgecolor='w', label="USA")
  l.yaxis.set_major_formatter(FuncFormatter(lambda x,pos: "%sM" % str(int(x)/1000000)[-2:] ))
  l.set_ylabel("USA")
  
  r = plt.subplot(2,1,2, sharex=l)
  plt.grid(True)
  r.bar(start_austin, austin_count, width=width_austin, color='k', edgecolor='w', label="Austin")
  r.yaxis.set_major_formatter(FuncFormatter(lambda x,pos: "%sk" % str(int(x)/1000)[-2:] ))
  r.xaxis.set_major_formatter(FuncFormatter(lambda x,pos: "%sk" % str(int(x)/1000) ))
  r.set_ylabel("Austin")
  r.set_xlabel("Household Income ($)")

  ticklabels = l.get_xticklabels()
  setp(ticklabels, visible=False)  
  
  plt.subplots_adjust(right=.95, top=.94, bottom=.2, left=.1)
  
  show()

if __name__ == "__main__":
  sys.exit(main())
