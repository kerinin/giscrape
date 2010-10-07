from datetime import * 

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals, log

import items
import orm

log.start()
  
class SQLBackend(object):
  
  def __init__(self):
    dispatcher.connect(self.engine_started, signal=signals.engine_started)
    dispatcher.connect(self.engine_stopped, signal=signals.engine_stopped)
    dispatcher.connect(self.item_passed, signal=signals.item_passed)
      
  def engine_started(self):
    orm.metadata.create_all(self.engine) 
      
  def engine_stopped(self):
    pass
      
  def item_passed(self, item, spider, output):
    session = orm.Session()
    
    try:
      if( isinstance(output, items.RentalItem) ):
        obj = orm.Rental(**output )
      elif( isinstance(output, items.SaleItem) ):
        obj = orm.Sale( **output )
      elif( isinstance(output, items.SoldItem) ):
        obj = orm.Sold( **output )
      else:
        raise orm.Fail, 'unknown data type'
    except orm.Fail:
      log.msg("SQL handling failed")
    else:
      obj.last_crawl = datetime.now()
      session.add( obj )
      session.commit()
      
