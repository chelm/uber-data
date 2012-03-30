import numpy as np 
import math
from datetime import datetime
import os.path

class Model:

  def __init__(self, bbox, matrix_file=None, nhours=None):
    """ A simple matrix based prediction grid

        a time weighted grid for determining travel times
        based of a series x/y pairs and times

        note: uses a euclidean distance model to linearly assign time based on two 
          arbitrary xy pairs and an associated time 
    """
    self.bbox = bbox

    if matrix_file != None: 
      self.matrix = np.load(matrix_file)
      self.width  = self.matrix.shape[1]
      self.height = self.matrix.shape[0]
      self.nhours = self.matrix.shape[2]

    else: 
      self.width  = 1000 
      self.height = 1000 
      self.nhours = nhours
      self.matrix = np.zeros((self.width, self.height, self.nhours))


  def save(self, file):
    np.save(file, self.matrix)    


  def hour(self, time):
    """ 
    Returns the hour from a time stamps 
    index of 0 to 23

    >>> m = Model( [-122, 38, -121, 37], './data/time_travel.npy' )
    >>> m.hour("2007-01-07T10:54:50+00:00")
    10
    """
    return self.time(time).hour


  def time(self, timestamp):
    """
    Returns a time object 
       
    >>> m = Model( [-122, 38, -121, 37], './data/time_travel.npy' )
    >>> t = m.time("2007-01-07T10:54:50+00:00")
    >>> print t
    2007-01-07 10:54:50
    """
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S+00:00")


  def time_diff(self, t1, t2):
    """ Differences two times and returns the delta seconds

    >>> m = Model( [-122, 38, -121, 37], './data/time_travel.npy' )
    >>> d = m.time_diff("2007-01-07T10:54:50+00:00", "2007-01-07T10:59:30+00:00")
    >>> print d
    280
    
    """
    diff = self.time(t2) - self.time(t1)
    return diff.seconds


  def yx(self, lat, lon):
    """ Convert lat lon into pixels 

    >>> m = Model( [-122.5, 37.5, -122, 38], './data/time_travel.npy' )
    >>> yx = m.yx(37.75, -122.25)
    >>> print yx[0], yx[1]
    500 500

    """
    y = int( math.floor( (self.bbox[3] - float(lat)) * (self.height / (self.bbox[3] - self.bbox[1])) ) )
    x = int( math.floor( self.width * (abs(self.bbox[0] - float(lon)) / abs(self.bbox[0] - self.bbox[2])) ) )
    return [y, x]


  def train(self, p1, p2):
    """ Trains the model with two points

        uses the time diff and delta xy to linearly 
        adjust time weights per cell   

    >>> m = Model( [-122, 38, -121, 37], './data/time_travel.npy' )  
    """
    xy1 = self.yx( p1[2], p1[3] ) 
    xy2 = self.yx( p2[2], p2[3] )

    hour = self.hour( p2[1] )
    delta = self.time_diff( p1[1], p2[1])

    # update the matrix model
    self.learn(xy1, xy2, hour, float(delta))


  def vector(self, p1, p2, dx, dy ):
    """ returns a pair vectors that we can use to extract times from the grid 

    >>> m = Model( [-122, 38, -121, 37], './data/time_travel.npy' )
    >>> m.vector([200, 200], [202, 202], 2, 2)
    (array([200, 201]), array([200, 201]))
    """
    #x = [ p1[1] ] if dx == 0 else np.arange( min( p1[1], p1[1] + dx ), max( p1[1], p1[1] + dx ) )
    #y = [ p1[0] ] if dy == 0 else np.arange( min( p1[0], p1[0] + dy ), max( p1[0], p1[0] + dy ) )
    x = [ p1[1] ] if dx == 0 else list( xrange( min( p1[1], p1[1] + dx ), max( p1[1], p1[1] + dx ) ) )
    y = [ p1[0] ] if dy == 0 else list( xrange( min( p1[0], p1[0] + dy ), max( p1[0], p1[0] + dy ) ) )
    return x, y


  def learn(self, p1, p2, t_index, delta):
    """ updates the matrix using 2 vectors for x,y
  
    Linear dist. of times per cell

    >>> m = Model( [-122, 38, -121, 37], './data/time_travel.npy' )
    """
    dx = p1[1] - p2[1] + 1
    dy = p1[0] - p2[0] + 1

    if abs(dx) + abs(dy) == 0:
      # update the p2 cell to avoid a double count
      x, y = p2[1], p2[0]
      val = self.matrix[x, y, t_index]

      if val == 0:
        self.matrix[x, y, t_index] = delta 
      else:
        self.matrix[x, y, t_index] = ( val + delta ) / 2

    else:
      t_per_cell = (abs(dx) + abs(dy)) / delta if delta else 0
      x, y = self.vector(p1, p2, dx, dy)
      try: 
        val = self.matrix[x, y, t_index]
        self.matrix[x, y, t_index] = ( val + t_per_cell ) / 2 
      except: 
        pass
      

  
  def predict(self, loc1, loc2, time=None):
    """ Predicts travel time across the grid 

    >>> m = Model( [-122, 38, -121, 37], './data/time_travel.npy' )
    >>> m.predict((37.795521, -122.419347), (37.795679, -122.409885), '2007-01-02T04:24:23+00:00')
    3.22 minutes
    """
    p1 = self.yx(loc1[0], loc1[1])
    p2 = self.yx(loc2[0], loc2[1])
    dx = p1[1] - p2[1] + 1
    dy = p1[0] - p2[0] + 1

    x, y = self.vector(p1, p2, dx, dy)

    if time: 
      t_index = self.hour(time)
      travel_time = np.sum(self.matrix[x, y, t_index])
    else:
      travel_time = np.sum(( np.sum(self.matrix, axis=2) / 24)[x, y])
    
    print round(travel_time,2), 'minutes'



  def visualize(self):
    """ create a 3D view of the matrix for each time

    """
    pass



if __name__ == "__main__":
  import doctest
  doctest.testmod()
