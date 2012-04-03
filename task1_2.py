import gzip 
import os.path 
from model import Model

def predict(m):
  points = [
    [ (37.795521, -122.419347), (37.795679, -122.409885), "2007-01-02T10:54:50+00:00"],
    [ (37.782551, -122.445368), (37.786956, -122.440279), "2007-01-05T10:54:50+00:00"],
    [ (37.800224, -122.433520), (37.800066, -122.436167), "2007-01-10T10:54:50+00:00"]
  ]

  print 'total1, total2' 
  for point in points:
    print (', ').join([m.predict( point[0], point[1]), m.predict( point[0], point[1], point[2])])




if __name__ == '__main__':
  
  file = './time_travel.npy'
  bbox = [-122.5, 37.5, -122, 38]
  frames = 7
  width, height = 1000, 1000

  # create and train a model if the file isnt there 
  if not os.path.exists(file):
    m = Model( bbox, width, height, None, frames )
    gps = gzip.open('all.tsv.gz', 'r').readlines()
  
    # loop over the points 
    for i in xrange(1, len(gps)):
      p2 = gps[i].strip().split('\t')
      p1 = gps[i-1].strip().split('\t')
      print p1
  
      # only train the model with points on the same track (ID)
      if p1[0] == p2[0]:
        m.train( p1, p2, int( p1[1][8:10] )-1 )
  
  
    print 'Finished training...now save'
    #m.visualize()
    m.save(file)
    predict(m)
  
  else:
    m = Model( bbox, width, height, file )
    predict(m)
    #for i in range(frames):
    #  print i
    #  m.visualize(i)
