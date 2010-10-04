from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals, log

from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker

import items
import orm

log.start()

class Fail(StandardError):
  pass
  
class SQLBackend(object):
  
  def __init__(self):
    dispatcher.connect(self.engine_started, signal=signals.engine_started)
    dispatcher.connect(self.engine_stopped, signal=signals.engine_stopped)
    dispatcher.connect(self.item_passed, signal=signals.item_passed)
      
  def engine_started(self):
    self.engine = create_engine('postgresql://postgres:kundera2747@localhost/gisdb', echo=True)
    self.metadata = orm.Base.metadata
    self.metadata.create_all(self.engine) 
    self.Session = sessionmaker(bind=self.engine)
      
  def engine_stopped(self):
    pass
      
  def item_passed(self, item, spider, output):
    session = self.Session()
    
    try:
      if( isinstance(output, items.RentalItem) ):
        obj = orm.Rental(**output )
      elif( isinstance(output, items.SaleItem) ):
        obj = orm.Sale( **output )
      else:
        raise Fail, 'unknown data type'
    except Fail:
      log.msg("SQL handling failed")
    else:
      session.add( obj )
      session.commit()
      
