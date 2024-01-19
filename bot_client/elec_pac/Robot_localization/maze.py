# Grid tiles
X = 1
o = 0

grid = [[X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X], # 0
        [X,o,o,o,o,X,X,o,o,o,o,X,X,X,X,X,o,X,X,X,X,X,o,o,o,o,o,o,o,o,X],
        [X,o,X,X,o,X,X,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,o,X,X,X,o,X],
        [X,o,X,X,o,o,o,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,o,X,X,X,o,X],
        [X,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,o,X,X,X,o,X],
        [X,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,o,X,X,X,o,X], # 5
        [X,o,X,X,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,X],
        [X,o,X,X,X,X,X,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,X,X,X,o,X,X,X,o,X],
        [X,o,X,X,X,X,X,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,X,X,X,o,X,X,X,o,X],
        [X,o,X,X,o,o,o,o,X,X,o,o,o,o,o,o,o,o,o,o,X,X,o,o,o,o,X,X,X,o,X],
        [X,o,X,X,o,X,X,o,X,X,o,X,X,o,X,X,X,X,X,o,X,X,o,X,X,o,X,X,X,o,X], # 10
        [X,o,X,X,o,X,X,o,X,X,o,X,X,o,X,X,X,X,X,o,X,X,o,X,X,o,X,X,X,o,X],
        [X,o,o,o,o,X,X,o,o,o,o,X,X,o,X,X,X,X,X,o,o,o,o,X,X,o,o,o,o,o,X],
        [X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,X,X,X],
        [X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,X,X,X],
        [X,o,o,o,o,X,X,o,o,o,o,X,X,o,X,X,X,X,X,o,o,o,o,X,X,o,o,o,o,o,X], # 15
        [X,o,X,X,o,X,X,o,X,X,o,X,X,o,X,X,X,X,X,o,X,X,o,X,X,o,X,X,X,o,X],
        [X,o,X,X,o,X,X,o,X,X,o,X,X,o,X,X,X,X,X,o,X,X,o,X,X,o,X,X,X,o,X],
        [X,o,X,X,o,o,o,o,X,X,o,o,o,o,o,o,o,o,o,o,X,X,o,o,o,o,X,X,X,o,X],
        [X,o,X,X,X,X,X,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,X,X,X,o,X,X,X,o,X],
        [X,o,X,X,X,X,X,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,X,X,X,o,X,X,X,o,X], # 20
        [X,o,X,X,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,X],
        [X,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,o,X,X,X,o,X],
        [X,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,o,X,X,X,o,X],
        [X,o,X,X,o,o,o,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,o,X,X,X,o,X],
        [X,o,X,X,o,X,X,o,X,X,o,X,X,X,X,X,o,X,X,X,X,X,o,X,X,o,X,X,X,o,X], # 25
        [X,o,o,o,o,X,X,o,o,o,o,X,X,X,X,X,o,X,X,X,X,X,o,o,o,o,o,o,o,o,X],
        [X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X]]
#        |         |         |         |         |         |         |
#        0         5        10        15       20         25       30

# Double the size of the grid
new_rows = len(grid) * 2
new_cols = len(grid[0]) * 2
expanded_grid = [[X] * new_cols for _ in range(new_rows)]

# Copy the old grid into the expanded grid
for i in range(new_rows):
    for j in range(new_cols):
        expanded_grid[i][j] = grid[i // 2][j // 2]

# Dilate the o tiles
dilated_grid = [row.copy() for row in expanded_grid]
for i in range(1, new_rows - 1):
    for j in range(1, new_cols - 1):
        if expanded_grid[i][j] == o:
            # Set the nine neighbors to o
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    dilated_grid[i + di][j + dj] = o

maze = dilated_grid