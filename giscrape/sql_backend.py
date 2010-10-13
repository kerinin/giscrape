from datetime import * 

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals, log

import sqlalchemy

import items
import orm

log.start()
session = orm.Session()
	
class SQLBackend(object):
  
  def __init__(self):
    dispatcher.connect(self.engine_started, signal=signals.engine_started)
    dispatcher.connect(self.engine_stopped, signal=signals.engine_stopped)
    dispatcher.connect(self.item_passed, signal=signals.item_passed)
      
  def engine_started(self):
    orm.metadata.create_all() 
      
  def engine_stopped(self):
    pass
      
  def item_passed(self, item, spider, output):
    try:
      if( isinstance(output, items.RentalItem) ):
        obj =  orm.Rental(**output)
      elif( isinstance(output, items.SaleItem) ):
        obj =  orm.Listing(**output)
      elif( isinstance(output, items.ListingItem) ):
        obj =  orm.Listing(**output)
      elif( isinstance(output, items.TCADParcelItem) ):
      
        improvements = output['improvements']
        segments = output['segments']
        historical_values = output['historical_values']

        del(output['improvements'])
        del(output['segments'])
        del(output['historical_values'])
        
        obj = orm.TCAD_2010(**output)
      
        for i in improvements:
          orm.TCADImprovement(parcel = obj, **i)
        for i in segments:
          seg = orm.TCADSegment(**i)
          session.merge( seg )       
        for i in historical_values:
          orm.TCADValueHistory(parcel = obj, **i)

      else:
        raise orm.Fail, 'unknown data type'
    except orm.Fail:
      log.msg("SQL handling failed")
    else:
      obj.last_crawl = datetime.now()

      session.merge(obj)
      session.commit()
      
