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
      elif( isinstance(output, items.PersonItem) ):
        if 'age' in output.keys() and len(output['age']) == 1:
          birth_year = (datetime.now() - timedelta(days=365*int(output['age'][0]))).year
          del output['age']
          prop = session.query(orm.TCAD_2010).get( int( output['prop_ref'][0] ) )
          del output['prop_ref']
          
          ref = session.query(orm.Person).filter(orm.Person.first_name == output['first_name'][0]).filter(orm.Person.last_name == output['last_name'][0]).filter(orm.Person.city == output['city'][0]).filter(orm.Person.state == output['state'][0]).filter(orm.Person.zipcode == output['zipcode'][0]).first()
          if ref:
            obj = orm.Person(id=ref.id, birth_year = birth_year, **output)
          else:
            obj = orm.Person(birth_year = birth_year, **output)
            
          prop.person = obj
          session.merge(prop)
          
      elif( isinstance(output, items.TCADParcelItem) ):
        if 'prop_id' in output.keys():
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
            except sqlalchemy.exc.IntegrityError:
              print "Improvements already Processed"
              session.rollback()
              
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
          print "prop_id not found"                                             

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
      
