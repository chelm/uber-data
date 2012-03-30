import gzip 
import os.path 
from model import Model


file = './time_travel.npy'
bbox = [-122.5, 37.5, -122, 38]
nhours = 24

if not os.path.exists(file):
  m = Model( bbox, None, nhours )
  gps = gzip.open('all.tsv.gz', 'r').readlines()

  for i in xrange(1, len(gps)):
    p2 = gps[i].split('\t')
    p1 = gps[i-1].split('\t')

    if p1[0] == p2[0]:
      m.train( p1, p2 )


  print 'Finished training...now save'
  #m.visualize()
  m.save(file)
  m.predict( (37.795521, -122.419347), (37.795679, -122.409885))
  m.predict( (37.782551, -122.445368), (37.786956, -122.440279))
  m.predict( (37.800224, -122.433520), (37.800066, -122.436167))

else:
  m = Model( bbox, file )
  #m.visualize()
  m.predict( (37.795521, -122.419347), (37.795679, -122.409885))
  m.predict( (37.782551, -122.445368), (37.786956, -122.440279))
  m.predict( (37.800224, -122.433520), (37.800066, -122.436167))
