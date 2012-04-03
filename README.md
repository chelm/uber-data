# Playing with Uber GPS tracks in SF 

## Task 1 & 2

### Problem: 

Develop and train a model that can predict travel times across SF. 

### Approach: 

I used a time weighted, grid based approach to solve this problem. This is accomplished with the help of NumPy and its awesome multi-dimensional arrays. The general idea is to loop over each point in the GPS data and operate on pairs of locations, calculating the distance and the a time delta. Using a very simple euclidean distance algorithm we can linearly divide the total time difference across each cell the path crosses. Essentially we train each cell by modulating its time-weight based on the time it take to cross it. Once the model is trained I save it to disk so we can use it to predict times very quickly. Prediction re-uses the distance/vector algorithm to traverse a path and sum each cell time the path crosses. 

One thing to note is the structure of the nd-array. Its a 1000 x 1000 x 7 grid over SF. Each coordinate pair trains on an daily index (the z-axis, 0 to 7). To predict travel times without a given time/day the grid is simply averaged into a 2d array and used to predict. To predict at a given location and day the corresponding daily index grid is used. Originally I was using an hourly index, and easily modify the grid to add a fourth axis for hour. This might improve the accuracy.  

### Problems:

1. This approach just uses "as the crow flies" distance, which is less than perfect for a city.

2. By using only a daily index on the data we assume uniform temporal distribution throughout each. This is an obvious error, as traffic is highly dynamic yet petterned. Probably simple to correct by adding a fourth dimension to the matrix for time of day. 

3. A grid based solution works, but a node graph solution would probably be better. Id like to experiment with using a graph database as the adaptation model, would be interesting for sure.  

4. The training is slow, the time diff fn is to blame for this. If I create a time diff that was avoided using the time_delta fn in datetime itd be faster. 

### Running:
  
  > python task1_2.py

### Results: 

* Task 1:

  * 
  *
  *

* Task 2:

  *
  *
  *


## Task 3

### Problem: 

Using the 25k GPS tracks can I think of way to detect errors/outliers and "scrub" them from any given GPS track. 

### Approach: 

I chose to treat this problem as an distance-threshold problem where any point that was further from the previous point than given a threshold would be dropped from the track. The goal then is to eliminate the highest number points while minimizing the amount of total time lost in GPS track. All this solution does is compute distances and drops points if thy cross a given threshold.  

I think Ive got a pretty solid was to solve this problem though. Its simple and solid solution that works.  

### Problems: 

1. This is a pretty rough and simple way of solving this problem, and there are several issues with this. It doesnt solve the problem of stationary sensors that would cause problems with the ETA algorithm.  

2. Could / Should use a combination of bearing and distance to more accurately drop points. 

Notes: One thing I noticed was that one track "18880" had a lot of dropped points. It turned out there was something funky. Several points share the same lat/lon: 37.600135, -122.383066. This is most likely an error, but I was curious so I made a simple map of this GPS track. See http://geocommons.com/maps/154890 - there is Prelim, dirty version of the track and a cleaned version.    

### Running the code:

  > python task3.py 

Results:  

* 21 Points are dropped at a threshold of .1 degrees 
* 26 Points are dropped at a threshold of .05 degrees 
* 48 Points are dropped at a threshold of .025 degrees 
* 135 Points are dropped at a threshold of .0125 degrees 

## Visualization  
