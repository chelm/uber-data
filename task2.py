import os.path 
from model import Model


file = './data/time_travel.npy'
bbox = [-122.5, 37.5, -122, 38]
nhours = 24

if not os.path.exists(file):
  m = Model( bbox, None, nhours )
  gps = open('./data/uber_gps_tsv/all.tsv', 'r').readlines()

  for i in xrange(1, len(gps)):
    point1 = gps[i].split('\t')
    print point1

    try: 
      if gps[i+1]:
        point2 = gps[i+1].split('\t')
        if point1[0] == point2[0]:
          m.train( point1, point2 )
    except:
      pass 

  print 'Finished training...now save'
  #m.visualize()
  m.save(file)
  m.predict( (37.795521, -122.419347), (37.795679, -122.409885), '2007-01-02T04:24:23+00:00')

else:
  m = Model( bbox, file )
  m.predict( (37.795521, -122.419347), (37.795679, -122.409885), '2007-01-02T04:24:23+00:00')
  #m.predict( (37.782551, -122.445368), (37.786956, -122.440279), '2007-01-07T10:56:58+00:00')
  m.predict( (37.800224, -122.433520), (37.800066, -122.436167)) # , '2007-01-06T06:22:35+00:00')
  #00001 2007-01-07T10:54:50+00:00 37.782551 -122.445368
  #00001 2007-01-07T10:56:58+00:00 37.786956 -122.440279

  #00002 2007-01-06T06:22:35+00:00 37.800224 -122.433520
  #00002 2007-01-06T06:25:03+00:00 37.800066 -122.436167
