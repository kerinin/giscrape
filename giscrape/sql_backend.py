from datetime import * 

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals, log

import sqlalchemy

import items
import orm

log.start()
session = orm.Session()

def upsert(model,values):
	try:
		obj = session.query(model).find(model.url == values['url'])
		obj.update(**values)
	except sqlalchemy.orm.exc.NoResultFound:
		obj = model(**values)
	return obj
	
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
    try:
      if( isinstance(output, items.RentalItem) ):
        obj = upsert(orm.Rental, output )
      elif( isinstance(output, items.SaleItem) ):
        obj = upsert(orm.Sale, output )
      elif( isinstance(output, items.ListingItem) ):
        obj = upsert(orm.Listing, output )
      else:
        raise orm.Fail, 'unknown data type'
    except orm.Fail:
      log.msg("SQL handling failed")
    else:
      obj.last_crawl = datetime.now()
      session.add( obj )
      session.commit()
      
