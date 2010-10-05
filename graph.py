#! /usr/bin/env python

import sys, getopt, math, datetime, os
import locale

from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker

from numpy import *
from pylab import *
from matplotlib.ticker import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from giscrape import orm
from giscrape.orm import *

_Functions = ['run','sale_price_distribution','rental_price_distribution']
	
engine = create_engine('postgresql://postgres:kundera2747@localhost/gisdb', echo=True)
metadata = orm.Base.metadata
metadata.create_all(engine) 
Session = sessionmaker(bind=engine)
  
locale.setlocale(locale.LC_ALL)
mFormatter = ticker.FuncFormatter(lambda x,pos: str(x/1000000.0)+'M' )
fig = plt.figure()

def run():
  sale_price_distribution(fig.add_subplot(1,2,1), False)
  rental_price_distribution(fig.add_subplot(1,2,2), False)
  
  show()
  
def sale_price_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):
  session = Session()
    
  trim = int(session.query(Sale).count()/50.0)
  price_max = int( session.query(Sale).filter(Sale.price != None).order_by(-Sale.price)[trim].price )
  price_min = int( session.query(Sale).filter(Sale.price != None).order_by(Sale.price)[trim].price )
  step = int( (price_max-price_min)/100.0 )

  X = range(price_min, price_max, step)
  Y = [ session.query(Sale).filter(Sale.price >= x).filter(Sale.price < x+step).count() for x in X ]

  ax.bar(X,Y, width=step, color='g')
  ax.set_title("Home Availability by Price")
  ax.set_ylabel("Units Available")
  ax.set_xlabel("Asking Price (Million $)")
  ax.grid(True)
  ax.axis([price_min,price_max,None,None])
  ax.xaxis.set_major_formatter(mFormatter)
  
  if to_show:
    show()
  
def rental_price_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):
  session = Session()
  
  trim = int(session.query(Rental).count()/50.0)
  price_max = int( session.query(Rental).filter(Rental.price != None).order_by(-Rental.price)[trim].price )
  price_min = int( session.query(Rental).filter(Rental.price != None).order_by(Rental.price)[trim].price )
  step = int( (price_max-price_min)/100.0 )

  X = range(price_min, price_max, step)
  Y = [ session.query(Rental).filter(Rental.price >= x).filter(Rental.price < x+step).count() for x in X ]
  
  ax.bar(X,Y, width=step, color='g')
  ax.set_title("Rental Availability by Price")
  ax.set_ylabel("Units Available")
  ax.set_xlabel("Monthly Rent ($)")
  ax.grid(True)
  ax.axis([price_min,price_max,None,None])

  if to_show:
    show()

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
