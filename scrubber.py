import math
from datetime import datetime
import os.path

class Scrubber:

  def __init__(self, thresh):
    """ A line scrubber that detects outliers based on a given distance treshold 

        computes the distance between two coordinate pairs 
        drops the second if the threshold is passed

        goal: to drop the highest number of points while minimizing changes in total track time 

        note: uses a euclidean distance model 
    """
    self.thresh = thresh

  def yx(self, lat, lon):
    """ Convert lat lon into pixels 

    >>> s = Scrubber( [-122.5, 37.5, -122, 38], 5)
    >>> yx = s.yx(37.75, -122.25)
    >>> print yx[0], yx[1]
    500 500

    """
    y = int( math.floor( (self.bbox[3] - float(lat)) * (self.height / (self.bbox[3] - self.bbox[1])) ) )
    x = int( math.floor( self.width * (abs(self.bbox[0] - float(lon)) / abs(self.bbox[0] - self.bbox[2])) ) )
    return [y, x]

  def dist(self, p1, p2):
    """ Simple euclidean distance between two points 

    >>> s = Scrubber( [-122.5, 37.5, -122, 38], 5)
    >>> p1 = s.yx(37.75, -122.25)
    >>> p2 = s.yx(37.77, -122.27)
    >>> s.dist(p1,p2)
    57
    >>> s.dist(p1,p1)
    0
    """
    d = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    return d

  def keep(self, p1, p2):
    """ Tests two points 
    
    >>> s = Scrubber( [-122.5, 37.5, -122, 38], 5)
    >>> p1 = s.yx(37.75, -122.25)
    >>> p2 = s.yx(37.77, -122.27)
    >>> s.keep(p1, p2)
    False

    >>> s.keep(p1, p1)
    True
    """
    return (self.dist(p1, p2) < self.thresh)


if __name__ == "__main__":
  import doctest
  doctest.testmod()
