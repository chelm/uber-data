import gzip
import os.path
from scrubber import Scrubber 

s = Scrubber(.1)
file = './all.tsv.gz'

# Make sure we've got the data file locally 
if not os.path.exists(file):
  print 'Missing GPS data:', file 
else:
  gps = gzip.open(file, 'r').readlines()

  # secondary j iterator used to prevent doulbe testing / dropping of points 
  j = 0
  
  for i in xrange(1, len(gps)):
    j = i if j == len(gps) else j
      
    p1 = gps[j-1].strip().split('\t')
    p2 = gps[j].strip().split('\t')
  
    if (p1[0] == p2[0]):
  
      keep = s.keep( [ float(p1[2]), float(p1[3]) ], [ float(p2[2]), float(p2[3])] )
      if not keep:
        j += 1 
        print i, keep, p1, p2
  
    j += 1
