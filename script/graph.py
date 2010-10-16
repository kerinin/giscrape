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

_Functions = [
  'run',
  'appraisal_accuracy',
  'cost_per_sf_vs_size',
  'age_vs_distance_scatter',
  'size_vs_distance_scatter',
  'size_vs_distance',
  'cost_per_sf_vs_distance',
  'cost_per_sf_vs_distance_scatter',
  'cost_vs_distance_scatter',
  'cost_vs_distance',
  'size_vs_age',
  'new_sale_size_distribution',
  'new_cost_per_sf_distribution',
  'new_sale_price_distribution',
  'recent_median_cost_vs_age',
  'median_cost_vs_age',
  'sale_size_distribution',
  'rent_per_sf_distribution',
  'cost_per_sf_distribution',
  'sale_price_distribution',
  'rental_price_distribution']
	
engine = create_engine('postgresql://postgres:kundera2747@localhost/gisdb', echo=True)
metadata = orm.Base.metadata
metadata.create_all(engine) 
Session = sessionmaker(bind=engine)
  
locale.setlocale(locale.LC_ALL)
mFormatter = ticker.FuncFormatter(lambda x,pos: str(x/1000000.0)+'M' )
yFormatter = ticker.FuncFormatter(lambda x,pos: "'"+str(x)[-2:] )
fig = plt.figure()

def run():
  sale_price_distribution(fig.add_subplot(1,2,1), False)
  rental_price_distribution(fig.add_subplot(1,2,2), False)
  
  show()


# TCAD '08 doesn't include the size of the structure
def TCAD_improvement_cost_per_sf_vs_distance():

  
def appraisal_accuracy():

  
def cost_per_sf_vs_size():

  
def age_vs_distance_scatter():

  
def size_vs_distance_scatter():

  
def size_vs_distance():


def cost_per_sf_vs_distance_scatter():

  
def cost_per_sf_vs_distance():

  
def cost_vs_distance_scatter():

  
def cost_vs_distance():

def size_vs_age( ax = fig.add_subplot(1,1,1), to_show=True):


def new_sale_size_distribution( ax = fig.add_subplot(1,1,1), to_show = True):

  
def new_cost_per_sf_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):

  
def new_sale_price_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):

    
def recent_median_cost_vs_age( ax = fig.add_subplot(1,1,1), to_show=True):

  
def median_cost_vs_age( ax = fig.add_subplot(1,1,1), to_show=True):


def sale_size_distribution( ax = fig.add_subplot(1,1,1), to_show = True):

  
def rent_per_sf_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):

  
def cost_per_sf_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):


def sale_price_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):

  
def rental_price_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):


def help():
  print __doc__
  return 0
	
def process(arg='run'):
  if arg in _Functions:
    globals()[arg]()
	
class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
	  try:
		  opts, args = getopt.getopt(sys.argv[1:], "hl:d:", ["help","list=","database="])
	  except getopt.error, msg:
		  raise Usage(msg)
	
	  # process options
	  for o, a in opts:
		  if o in ("-h", "--help"):
			  for f in _Functions:
				  if f in args:
					  apply(f,(opts,args))
					  return 0
			  help()
	
	  # process arguments
	  for arg in args:
		  process(arg) # process() is defined elsewhere
  except Usage, err:
	  print >>sys.stderr, err.msg
	  print >>sys.stderr, "for help use --help"
	  return 2

if __name__ == "__main__":
  sys.exit(main())
