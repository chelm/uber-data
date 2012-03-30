# Playing with Uber GPS tracks in SF 

## Task 1 & 2

Problem: Develop and train a model that can predict travel times across SF. 

Approach: I used a time weighted, grid based approach to solve this problem. This is accomplished with the help of NumPy and its awesome multi-dimensional arrays. The general idea is to loop over each point in the GPS data and operate on pairs of locations, calculating the distance and the a time delta. Using a very simple euclidean distance algorithm we can linearly divide the total time difference across each cell the path crosses. Essentially we train each cell by modulating its time-weight based on the time it take to cross it. Once the model is trained I save it to disk so we can predict and test quickly. Prediction re-uses the distance/vector algorithm to traverse a path and sum each cells time. 

One thing to note is the structure of the nd-array. Its a 1000 x 1000 x 24 grid over SF. Each coordinate pair trains on an hourly index (the z-axis, 0 to 23). To predict travel times without a given time the grid is simply averaged into a 2d grid and used to predict. To predict at a given time only the hourly index grid is used. 

Problems:  

Running:
  
  > python task1.py

  > python task2.py  



## Task 3

Problem: Using the 25k GPS tracks can I think of way to detect errors/outliers and "scrub" them from any given GPS track. 

Approach: I chose to treat this problem as an distance-threshold problem where any point that was further from the previous point than given a threshold would be dropped from the track. The goal then is to eliminate the highest number points while minimizing the amount of total time lost in GPS track. All this solution does is compute distances and drops points if thy cross a given threshold.  

Problems: 

1. This is a pretty rough and simple way of solving this problem, and there are several issues with this. 

Notes: One thing I noticed was that one track "18880" had a lot of dropped points.  

Running the code:

  > python task3.py 

Results:  


## Visualization  
