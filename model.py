import numpy as np 
import math
from datetime import datetime, date
from PIL import Image
import os.path

class Model:

  def __init__(self, bbox, width=None, height=None, matrix_file=None, frames=None):
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
      self.frames = self.matrix.shape[2]

    else: 
      self.width  = width
      self.height = height 
      self.frames = frames
      self.matrix = np.zeros(( self.height, self.width, self.frames, 2))

    print self.matrix.shape


  def save(self, file):
    np.save(file, self.matrix)    


  def day(self, time):
    """ 
    Returns the hour from a time stamps 
    index of 0 to 23

    >>> m = Model( [-122, 38, -121, 37], './time_travel.npy' )
    >>> m.day("2007-01-07T10:54:50+00:00")
    6
    """
    return date.weekday(self.time(time)) 


  def time(self, timestamp):
    """
    Returns a time object 
       
    >>> m = Model( [-122, 38, -121, 37], './time_travel.npy' )
    >>> t = m.time("2007-01-07T10:54:50+00:00")
    >>> print t
    2007-01-07 10:54:50
    """
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S+00:00")


  def time_diff(self, t1, t2):
    """ Differences two times and returns the delta seconds

    >>> m = Model( [-122, 38, -121, 37], './time_travel.npy' )
    >>> d = m.time_diff("2007-01-07T10:54:50+00:00", "2007-01-07T10:59:30+00:00")
    >>> print d
    280
    
    """
    diff = abs(self.time(t2) - self.time(t1))
    return diff.seconds


  def yx(self, lat, lon):
    """ Convert lat lon into pixels 

    >>> m = Model( [-122.5, 37.5, -122, 38], './time_travel.npy' )
    >>> yx = m.yx(37.75, -122.25)
    >>> print yx[0], yx[1]
    500 500

    """
    y = int( math.floor( (self.bbox[3] - float(lat)) * (self.height / (self.bbox[3] - self.bbox[1])) ) )
    x = int( math.floor( self.width * (abs(self.bbox[0] - float(lon)) / abs(self.bbox[0] - self.bbox[2])) ) )
    return [y, x]

  def dist(self, p1, p2):
    """ Simple euclidean distance between two points 

    >>> m = Model( [-122.5, 37.5, -122, 38], './time_travel.npy')
    >>> p1 = m.yx(37.75, -122.25)
    >>> p2 = m.yx(37.77, -122.27)
    >>> m.dist(p1,p2)
    57.280013966478741
    >>> m.dist(p1,p1)
    0.0

    """
    return int( math.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2)) )
    


  def train(self, p1, p2, day):
    """ Trains the model with two points

        uses the time diff and delta xy to linearly 
        adjust time weights per cell   

    >>> m = Model( [-122, 38, -121, 37], './time_travel.npy' )  
    """
    xy1 = self.yx( p1[2], p1[3] ) 
    xy2 = self.yx( p2[2], p2[3] )

    #day = self.day( p2[1] )
    delta = self.time_diff( p1[1], p2[1])

    # update the matrix model
    self.learn(xy1, xy2, day, float(delta))


  def vector(self, p1, p2):
    """ returns a pair vectors that we can use to extract times from the grid 

    >>> m = Model( [-122, 38, -121, 37], './time_travel.npy' )
    >>> #m.vector([200, 200], [202, 202])
    >>> #([200, 201], [200, 201])
    >>> #sum(sum(m.matrix[[200, 201, 202], [200, 201, 202], :])) / 7
    >>> sum(sum(m.matrix[[109, 110, 111, 112, 113, 114, 115, 116, 117, 118], [434, 435, 436, 437, 438, 439, 440, 441], :])) / 7
    """
    dx = (p1[1] - p2[1]) + 1
    dy = (p1[0] - p2[0]) + 1

    x = [ p1[1] ] if dx == 0 else list( xrange( min( p1[1], p1[1]+dx ), max( p1[1], p1[1]+dx ) ) )
    y = [ p1[0] ] if dy == 0 else list( xrange( min( p1[0], p1[0]+dy ), max( p1[0], p1[0]+dy ) ) )
    
    return x, y


  def learn(self, p1, p2, t_index, delta):
    """ updates the matrix using 2 vectors for x,y
  
    Linear dist. of times per cell

    >>> m = Model( [-122, 38, -121, 37], './time_travel.npy' )
    """
    distance = self.dist(p1, p2)
    
    if distance == 0:
      x, y = p2[1], p2[0]
    else:
      x, y = self.vector( p1, p2 )
      delta = delta / (len(x)*len(y)) if delta else 0
    
    try:
      for px in x:
        for py in y:
          self.matrix[ py, px, t_index, 0] += delta
          self.matrix[ py, px, t_index, 1] += 1
    except:
      pass

  
  def predict(self, loc1, loc2, time=None):
    """ Predicts travel time across the grid 

    >>> m = Model( [-122.5, 37.5, -122, 38], './time_travel.npy' )
    >>> m.predict( (37.795521, -122.419347), (37.795679, -122.409885) )
    '00:02:40'
    """
    p1 = self.yx(loc1[0], loc1[1])
    p2 = self.yx(loc2[0], loc2[1])

    x, y = self.vector(p1, p2)
    travel_time = 0
    count = 0

    if time: 
      t_index = self.day(time) 
      for px in x:
        for py in y:
            travel_time += self.matrix[ py, px, t_index, 0] if ( self.matrix[ py, px, t_index, 1] == 0 ) else self.matrix[ py, px, t_index, 0]/self.matrix[ py, px, t_index, 1]
    else:
      for px in x:
        for py in y:
          travel_time += sum(self.matrix[ py, px, :, 0]) / sum(self.matrix[ py, px, :, 1])
  
    return self.timeFormat(int( travel_time ))


  def timeFormat(self, seconds):
    """ Simple formating function

    >>> m = Model( [-122, 38, -121, 37], './time_travel.npy' )
    >>> m.timeFormat( 244 )
    '00:04:04'
    """
    hours = seconds / 3600
    seconds -= 3600*hours
    minutes = seconds / 60
    seconds -= 60 * minutes
    return "%02d:%02d:%02d" % (hours, minutes, seconds)



  def visualize(self, index=None):
    """ create a 3D view of the matrix for each time

    """
    self.matrix.dtype = 'uint8'
    if index:
      I = self.matrix[:, :, index]
    else:
      I = np.sum( self.matrix, axis=2) / self.frames
      print I.shape
      I.dtype = 'uint8'
      #I.reshape(2000,4000)
      index = 'all'
    resultImage = Image.fromarray(I).convert('RGB')
    resultImage.save('uber.' + str(index) + '.png')
    pass



if __name__ == "__main__":
  import doctest
  doctest.testmod()
