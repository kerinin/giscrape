#! /usr/bin/env python

import sys, getopt, math, datetime, os
import locale

from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql.expression import *

from numpy import *
from pylab import *
from matplotlib.ticker import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from giscrape import orm
from giscrape.orm import *

_Functions = ['run','recent_median_cost_vs_age','median_cost_vs_age','sale_size_distribution','rent_per_sf_distribution','cost_per_sf_distribution','sale_price_distribution','rental_price_distribution']
	
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
  
#histogram array by distance - price/rent/floor area/age
#income distribution vs rent/cost distribution
#time to sell vs asking price
#time to sell vs size
#time to sell vs bed & baths
#median rent ratio by floor area (control for bed/bath? include bars?)
#floor area vs age

def recent_median_cost_vs_age( ax = fig.add_subplot(1,1,1), to_show=True):
  fig.suptitle("Asking Price Distribution by Age, 1996-2010", fontsize=18, weight='bold')
  
  session = Session()
  
  q = session.query(Sale).filter(Sale.year_built != None).filter(Sale.price != None).filter(Sale.year_built >= 1995)
  total = q.count()

  
  def prices(year):
    return [ x.price for x in q.filter('for_sale.year_built = %s' % year).all() ]
    
  X = arange(1996, 2011, 1)
  Y = [ prices(x) for x in X ]
  C = [ len(y) for y in Y ]
  

  ax.set_title("Boxes show median and quartiles, lines show inner quartile range")   
  ax.set_xlabel("Year Built")
  p1=ax.plot(X,C,'--k', alpha=.5, zorder=-1)
  ax.set_ylabel('Sample Size')
  
  ax2 = ax.twinx() 
  ax2.boxplot(Y, sym='', whis=1.5, positions=X, widths=.5)
  ax2.set_ylabel("Asking Price Distribution ($)")
  ax2.grid(True)
  ax2.yaxis.set_major_formatter(mFormatter)
  ax2.xaxis.set_major_formatter(yFormatter)
  ax2.axis([1995,2011,None,None])
  
  legend([p1],['Sample Size'], loc=2)
  show()  
  
def median_cost_vs_age( ax = fig.add_subplot(1,1,1), to_show=True):
  fig.suptitle("Asking Price Distribution by Age", fontsize=18, weight='bold')
  
  session = Session()
  
  q = session.query(Sale).filter(Sale.year_built != None).filter(Sale.price != None)
  total = q.count()
  trim = int( total * .01 )
  first_date = q.order_by(asc(Sale.year_built))[trim].year_built
  last_date = q.order_by(desc(Sale.year_built)).first().year_built
  step = int((last_date - first_date)/12. )
  
  def prices(start,end):
    return [ x.price for x in q.filter('for_sale.year_built >= %s' % start).filter('for_sale.year_built < %s' % end).all() ]
    
  X = arange(first_date, last_date, step)
  Y = [ prices(x,x+step) for x in X ]
  C = [ len(y) for y in Y ]
  

  ax.set_title("Boxes show median and quartiles, lines show inner quartile range")   
  ax.set_xlabel("Year Built")
  p1=ax.plot(X,C,'--k', alpha=.5, zorder=-1)
  ax.set_ylabel('Sample Size')
  
  ax2 = ax.twinx() 
  ax2.boxplot(Y, sym='', whis=1.5, positions=X, widths=(.5*step))
  ax2.set_ylabel("Asking Price Distribution ($)")
  ax2.grid(True)
  ax2.axis([first_date-(step/2),last_date,None,None])
  ax2.yaxis.set_major_formatter(mFormatter)
  ax2.xaxis.set_major_formatter(yFormatter)
  
  legend([p1],['Sample Size'], loc=2)
  show()  

def sale_size_distribution( ax = fig.add_subplot(1,1,1), to_show = True):
  fig.suptitle("Home Size Distribution", fontsize=18, weight='bold')
  
  session = Session()
  
  area_query = session.query(Sale).filter(Sale.size != None)
  total = area_query.count()
  trim = int( total * .02 )
  max_area = area_query.order_by(desc(Sale.size))[trim].size
  min_area = area_query.order_by(asc(Sale.size)).first().size
  step = int( (max_area - min_area)/100.0 )
  
  X = arange(min_area, max_area, step)
  Y = [ area_query.filter("for_sale.size >= %s" % str(x)).filter("for_sale.size < %s" % str(x+step)).count() for x in X ]
  C = [ 100*float(area_query.filter("for_sale.size < %s" % str(x+step)).count())/total for x in X ]
  
  ax.bar(X,Y, width=step, color='c',edgecolor='c')
  
  ax.set_ylabel("Units Available")
  ax.set_xlabel("Size (sf)")
  
  ax2 = ax.twinx()
  ax2.plot(X,C,'--k')
  ax2.set_ylabel('Cumulative Units (%)')
  ax2.axis([min_area,max_area,None,None])
  
  show()
  
def rent_per_sf_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):
  fig.suptitle("Rent/sf Distribution", fontsize=18, weight='bold')
  session = Session()

  per_sf_query = session.query(Rental).filter(Rental.price != None).filter(Rental.size != None).order_by(asc(Rental.price / Rental.size))
  total_rentals = per_sf_query.count()
  trim = int( per_sf_query.count() * .01 )
  per_sf_min = float( per_sf_query.first().price / per_sf_query.first().size )
  per_sf_query = session.query(Rental).filter(Rental.price != None).filter(Rental.size != None).order_by(desc(Rental.price / Rental.size))
  per_sf_max = float( per_sf_query[trim].price / per_sf_query[trim].size )

  step = float( (per_sf_max-per_sf_min)/10.0 )
  print [per_sf_max,per_sf_min,step]

  X = arange(per_sf_min, per_sf_max, step)
  Y = [ per_sf_query.filter("rental.price / rental.size >= %s" % x).filter("rental.price / rental.size < %s" % (x + step)).count() for x in X ]
  C = array( [ per_sf_query.filter("rental.price / rental.size < %s" % (x + step)).count() for x in X ] )
    
  ax.bar(X,Y, width=step, color='y')
  
  ax.set_ylabel("Units Available")
  ax.set_xlabel("Monthly Rent / sf ($/sf)")
  
  ax2 = ax.twinx()
  ax2.plot(X,C,'--k')
  ax2.set_ylabel('Cumulative Units (%)')
  ax2.axis([per_sf_min,per_sf_max,None,None])
    
  show()
  
def cost_per_sf_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):
  fig.suptitle("Home Price/sf Distribution", fontsize=18, weight='bold')
  session = Session()

  per_sf_query = session.query(Sale).filter(Sale.price != None).filter(Sale.size != None).order_by(asc(Sale.price / Sale.size))
  trim = int( per_sf_query.count() * .01 )
  per_sf_min = int( per_sf_query.first().price / per_sf_query.first().size )
  per_sf_query = session.query(Sale).filter(Sale.price != None).filter(Sale.size != None).order_by(desc(Sale.price / Sale.size))
  per_sf_max = int( per_sf_query[trim].price / per_sf_query[trim].size )

  step = int( (per_sf_max-per_sf_min)/100.0 )

  X = arange(per_sf_min, per_sf_max, step)
  Y = [ per_sf_query.filter("for_sale.price / for_sale.size >= %s" % x).filter("for_sale.price / for_sale.size < %s" % (x + step)).count() for x in X ]
  C = [ per_sf_query.filter("for_sale.price / for_sale.size < %s" % (x + step)).count() for x in X ]
  
  ax.bar(X,Y, width=step, color='y')
  
  ax.set_ylabel("Units Available")
  ax.set_xlabel("Asking Price / sf ($/sf)")
  
  ax2 = ax.twinx()
  ax2.plot(X,C,'--k')
  ax2.set_ylabel('Cumulative Units')
  ax2.axis([per_sf_min,per_sf_max,None,None])
    
  show()

def sale_price_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):
  fig.suptitle("Home Availability by Price", fontsize=18, weight='bold')
  session = Session()
    
  trim = int(session.query(Sale).count()/50.0)
  price_max = int( session.query(Sale).filter(Sale.price != None).order_by(-Sale.price)[trim].price )
  price_min = int( session.query(Sale).filter(Sale.price != None).order_by(Sale.price)[trim].price )
  step = int( (price_max-price_min)/100.0 )

  X = range(price_min, price_max, step)
  Y = [ session.query(Sale).filter(Sale.price >= x).filter(Sale.price < x+step).count() for x in X ]
  C = [ session.query(Sale).filter(Sale.price < x).count() for x in X ]

  ax.bar(X,Y, width=step, color='g')
  ax.set_ylabel("Units Available")
  ax.set_xlabel("Asking Price (Million $)")
  ax.grid(True)
  ax.axis([price_min,price_max,None,None])
  ax.xaxis.set_major_formatter(mFormatter)
  
  ax2 = ax.twinx()
  ax2.plot(X,C,'--k')
  ax2.set_ylabel('Cumulative Units')
  ax2.axis([price_min,price_max,None,None])
  ax2.xaxis.set_major_formatter(mFormatter)
  
  if to_show:
    show()
  
def rental_price_distribution( ax = fig.add_subplot(1,1,1), to_show = True ):
  fig.suptitle("Rental Availability by Price", fontsize=18, weight='bold')
  session = Session()
  
  trim = int(session.query(Rental).count()/50.0)
  price_max = int( session.query(Rental).filter(Rental.price != None).order_by(-Rental.price)[trim].price )
  price_min = int( session.query(Rental).filter(Rental.price != None).order_by(Rental.price)[trim].price )
  step = int( (price_max-price_min)/100.0 )

  X = range(price_min, price_max, step)
  Y = [ session.query(Rental).filter(Rental.price >= x).filter(Rental.price < x+step).count() for x in X ]
  C = [ session.query(Rental).filter(Rental.price < x).count() for x in X ]
    
  ax.bar(X,Y, width=step, color='g')
  ax.set_ylabel("Units Available")
  ax.set_xlabel("Monthly Rent ($)")
  ax.grid(True)
  ax.axis([price_min,price_max,None,None])

  ax2 = ax.twinx()
  ax2.plot(X,C,'--k')
  ax2.set_ylabel('Cumulative Units')
  ax2.axis([price_min,price_max,None,None])
  
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
