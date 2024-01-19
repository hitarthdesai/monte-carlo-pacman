#This file contains all the functions for cleanliness
#In the algorithm we will deal with inches
from parameters import *

#Debug messages functions
def debug_message(msg):
    if debug==1:
        print(msg)
        time.sleep(sleep) 

#Recursive search function for grid boxes
def recursive_count(r, c, direction):
    # Check if the position is within the grid boundaries and is a non-wall position
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == 0:
        # Mark the current position as visited 
        grid[r][c] = -1  # Assuming -1 represents a visited position

        # Explore in the specified direction recursively
        if direction == "N":
            return 1 + recursive_count(r - 1, c, "N")
        elif direction == "S":
            return 1 + recursive_count(r + 1, c, "S")
        elif direction == "E":
            return 1 + recursive_count(r, c + 1, "E")
        elif direction == "W":
            return 1 + recursive_count(r, c - 1, "W")
    
    return 0
#This function finds the number of open grid boxes in all 4 directions for a given grid box
def count_surrounding(row, col):
    debug_message("We are now counting the number of available grids around us")

    if grid[row][col] == 1:
        return -1, -1, -1, -1  # If the current position is 'X', return zeros for all directions
    
    # Call the recursive function for each direction in the specified order
    count_top = recursive_count(row - 1, col, "N")
    count_bottom = recursive_count(row + 1, col, "S")
    count_right = recursive_count(row, col + 1, "E")
    count_left = recursive_count(row, col - 1, "W")

    return count_top, count_bottom, count_left, count_right


#This function returns the distance in inches from number fo grid boxes
#TODO: if space!=0, we need to add the distance from the center of the bot
def distance_from_grid(space):
    if space==0:
        return grid_size-(bot_len/2)
    else:
        #TODO: check this calculation
        return (space*grid_size+(grid_size-(bot_len/2)))
    
#Returns the closest n available grid boxes
def find_closest_n(row, col, n):
    debug_message("We are now finding the closest available grids around us")
    if grid[row][col] == 1:
        return []  # If the current position is 'X', return an empty list

    # Define a function to calculate the distance between two points
    def distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    # Sort the coordinates based on their distance from the specified row and column
    # sorted has O(nlogn) time complexity and uses Timsort for sorting
    sorted_o = sorted(open_coordinates, key=lambda point: distance((row, col), point))

    # Return the closest n coordinates
    return sorted_o[:n]

# Converting mm to inches
def mm_to_inches(mm):
    inches = mm / 25.4
    return inches

# Getting available grid boxes from inches
def inches_to_grid_spots(measurement):
    return (measurement // grid_size) + 1