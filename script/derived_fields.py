from giscrape.orm import *

def main(argv=None):

  s=Session()
  types = ['1ST','2ND','3RD','4TH','5TH','ADDL','BELOW','CONC','FBSMT','LOBBY','MEZZ','RSBLW']

  # Set 'new construction' bool for Value History
  for vh in s.query(TCADValueHistory).filter(TCADValueHistory.new_construction==None).all():
    vh.new_construction = bool( s.query(TCADSegment).join(TCADSegment.improvement).join(TCADImprovement.parcel).join(TCAD_2010.historical_values).filter(TCADSegment.year_built == vh.year).filter(TCADValueHistory.id == vh.id).filter(TCADSegment.type_code.in_(types)).count())
    if vh.new_construction:
      print "New Construction in %s: %s" % (vh.year, vh.parcel.prop_id)
    s.merge(vh)
    s.commit()

  # Label Value History with built area for that year
  for vh in s.query(TCADValueHistory).join(TCADValueHistory.parcel).filter(TCAD_2010.improvement_area != None).filter(TCADValueHistory.area == None).all():
    vh.area = s.query(TCADSegment).join(TCADSegment.improvement).join(TCADImprovement.parcel).join(TCAD_2010.historical_values).filter(TCADValueHistory.id == vh.id).filter(TCADSegment.type_code.in_(types)).filter(TCADSegment.year_built <= vh.year).value(func.sum(TCADSegment.area))
    print "Added %s area to %s: %s" % (vh.year, vh.parcel.prop_id, vh.area)
    s.merge(vh)
    s.commit()

  # Aggregate total improvement area for Parcel
  # NOTE: shouldn't be necessary
  for p in s.query(TCAD_2010).filter(TCAD_2010.improvement_area == None).join(TCAD_2010.improvements).all():
    p.improvement_area = s.query( TCADSegment ).join(TCADSegment.improvement).join(TCADImprovement.parcel).filter(TCADSegment.type_code.in_(types)).filter(TCAD_2010.gid == float(p.gid)).value(func.sum(TCADSegment.area))
    print "Parcel %s has improvement area %s" % (p.prop_id, p.improvement_area)
    s.merge(p)
    s.commit()


if __name__ == "__main__":
  sys.exit(main())
