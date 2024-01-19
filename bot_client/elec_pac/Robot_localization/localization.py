import logic
from parameters import *

if find_distance:
    input_str = input("Enter row and column separated by a comma (e.g., 1,1): ")
    row, col = map(int, input_str.split(','))

    if grid[row][col]==1:
        print("Thats a wall!")
    else:
        result_top, result_bottom, result_left, result_right = logic.count_surrounding(row, col)
        print(f"Number of spaces in NSEW are [{result_top},{result_bottom},{result_right},{result_left}]")
        logic.debug_message("Distance from grid")
        print(f"Space in inches in NSEW is [{logic.distance_from_grid(result_top)},{logic.distance_from_grid(result_bottom)},{logic.distance_from_grid(result_right)},{logic.distance_from_grid(result_left)}]")

if find_closest:
    input_str = input("Enter row, column and n separated by a comma (e.g., 6,7,4): ")
    row, col, n= map(int, input_str.split(','))

    if grid[row][col]==1:
        print("Thats a wall!")
    else:
        closest_o = logic.find_closest_n(row, col, n)
        print(f"The closest {n} available spots for position [{row}, {col}]: {closest_o}")


# Get user input for four lengths in millimeters
input_str = input("Enter TOF reading in millimeters separated by commas (eg: NSEW): ")
# 7 inches is 178mm
lengths_in_mm = [float(length) for length in input_str.split(',')]

if len(lengths_in_mm) != 4:
    print("Enter 4 values")
    sys.exit() #avoid using this type of exit

# Convert millimeters to inches for each length
lengths_in_inches = [logic.mm_to_inches(length) for length in lengths_in_mm]
# Convert inches to grid spots for each length
curr_grid_spots = [logic.inches_to_grid_spots(length) for length in lengths_in_inches]

# Display the results
if debug:
    for i in range(4):
        print(f"{lengths_in_mm[i]} millimeters is equal to {lengths_in_inches[i]:.2f} inches.")

print(f"Grids spots in NSEW are {curr_grid_spots}")

input_str = input("Enter row, column and n separated by a comma (e.g., 6,7,4): ")
row, col, n= map(int, input_str.split(','))

if grid[row][col]==1:
    print("Thats a wall!")
    sys.exit()

closest_o = logic.find_closest_n(grid, row, col, n)

# Now we have number of spaces in each direction and possible grid spots
for calculated_spot in closest_o:
    if curr_grid_spots == logic.count_surrounding(calculated_spot):
        print(f"We are in grid box {calculated_spot}")

print("We are screwed!")






