from datetime import * 

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals, log

import sqlalchemy

import items
import orm

log.start()
	
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
    session = orm.Session()
    obj = None
    try:
      if( isinstance(output, items.RentalItem) ):
        obj =  orm.Rental(**output)
      elif( isinstance(output, items.SaleItem) ):
        obj =  orm.Listing(**output)
      elif( isinstance(output, items.ListingItem) ):
        obj =  orm.Listing(**output)
      elif( isinstance(output, items.TCADParcelItem) ):
        parcel = session.query(orm.TCAD_2010).filter(orm.TCAD_2010.prop_id == int( output['prop_id'][0] ) )
        if parcel.count() == 1:
          try:
            improvements = output['improvements']
            del(output['improvements'])
            
            for i in improvements:
              imp = orm.TCADImprovement(parcel = parcel.first(), **i)
              session.merge( imp ) 
          except KeyError:
            print "No Improvements Found"
            
          try:
            segments = output['segments']
            del(output['segments'])
            
            for i in segments:
              seg = orm.TCADSegment(**i)
              session.merge( seg )
          except KeyError:
            print "No Segments Found"   
                      
          historical_values = output['historical_values']
          del(output['historical_values'])
          
          obj = orm.TCAD_2010(objectid = parcel.first().objectid, **output)

          for i in historical_values:
            orm.TCADValueHistory(parcel = obj, **i)
        else:
          print "duplicate / missing prop_id - not inserted"

      else:
        raise orm.Fail, 'unknown data type'
    except orm.Fail:
      log.msg("SQL handling failed")
    else:
      if obj:
        obj.last_crawl = datetime.now()

        session.merge(obj)
        session.commit()
      else:
        print "Duplicate handled"
      
