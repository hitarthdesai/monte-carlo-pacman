#Define all the parameters here 
import time
import sys
from maze import grid
find_distance=0  #Case if we want to find the availablle grid boxes
find_closest=1   #Case if we want to find closesnt n grod boxes
grid_size = 7    #size of each grid box in inches
bot_len = 4      #total length (in inches) between N and S of the robot
debug = 0        #option if we want to print debug messages
sleep = 1        #wait period in between each debug message (in seconds)

# Flatten the grid into a list of coordinates for open spaces
open_coordinates = [(r, c) for r, row in enumerate(grid) for c, val in enumerate(row) if val == 0]