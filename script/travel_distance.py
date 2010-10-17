from giscrape.orm import *
from google.directions import GoogleDirections

travel_type = None
lat = None
lon = None

from google.directions import GoogleDirections
gd = GoogleDirections('ABQIAAAAxBYO1IaeRmbM-69cgm4FNxTOoCsxsJIZtfDnfwGVFTuk5s_7vhTNDQwxRTn-UxHFgGD1WfSxQP6nrQ')
res=gd.query('30.267,-97.743', '35.77,-78.6386',mode="walking")


def help():
  print "python travel_distance.py [all|car|bike|walk] --lat=<latitude> --lon=<longitude>"
  print __doc__
  return 0
	
class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
	  try:
		  opts, args = getopt.getopt(sys.argv[1:], "h", ["help","lat=","lon="])
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
	
    
    
  except Usage, err:
	  print >>sys.stderr, err.msg
	  print >>sys.stderr, "for help use --help"
	  return 2

  gd = GoogleDirections() 
  
  res = gd.query('%s,%s' % (), '35.77,-78.6386')
  
if __name__ == "__main__":
  sys.exit(main()))
