from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals, log

from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker

import items
import orm

log.start()

class SQLBackend(object):
    
    def __init__(self):
        dispatcher.connect(self.engine_started, signal=signals.engine_started)
        dispatcher.connect(self.engine_stopped, signal=signals.engine_stopped)
        dispatcher.connect(self.item_passed, signal=signals.item_passed)
        
    def engine_started(self):
        log.msg("opening database connection")
        
        self.engine = create_engine('postgresql://postgres:kundera2747@localhost/gisdb', echo=True)
        self.metadata = orm.metadata
        self.metadata.create_all(self.engine) 
        self.Session = sessionmaker(bind=self.engine)
        
        mapper(items.RentalItem, orm.rental_table)
        mapper(items.SaleItem, orm.sale_table)
        
    def engine_stopped(self):
        pass
        
    def item_passed(self, item, spider, output):
        session = self.Session()
        
        session.add(output)
        session.commit()
