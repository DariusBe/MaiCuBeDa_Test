import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# global variables:
grid_size = 150
trail_decay = 0.9
rotation_angle = 22.5
sensor_angles = 45
sensor_distances = 9 #9px


# define numpy 2D Vector
class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Physarum:
    def __init__(self, position, heading):
        self.position = position
        self.heading = heading

# initialize the grid
grid = np.zeros((grid_size, grid_size))
grid[grid_size//2, grid_size//2] = 1

def update(last_grid):
    grid = last_grid.copy()
    # Loop over all cells in the grid
    for x in range(0, grid_size-1):
        for y in range(0, grid_size-1):
            if grid[x, y] == 1:
                grid[max(x-1, 0), y] = 1
                grid[x, y] = 0
    return grid


# Create the animation
fig = plt.figure()
im = plt.imshow(grid, cmap='gray', animated=True)
def animate(*args):
    global grid
    grid = update(grid)
    im.set_array(grid)
    return im,
ani = animation.FuncAnimation(fig, animate, interval=10, blit=True)
plt.show()


'''
# Initialize grid
#grid = np.random.choice([0, 1], size=(50, 50))
grid = np.random.choice([0,0,0,0,1], size=(150, 150))


# Define the rules
def update(grid):
    new_grid = grid.copy()
    # Loop over all cells in the grid
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            # If the cell is empty, leave it empty
            if grid[i, j] == 0:
                new_grid[i, j] = 0
            # If the cell is full, check if it has 5 or more neighbors
            else:
                neighbors = grid[i - 1:i + 2, j - 1:j + 2]
                # If it has 3 or more neighbors, fill the cell
                if np.sum(neighbors) >= 3:
                    new_grid[i, j] = 1
                # If it has 8 neighbors, empty the neighbors
                else:
                    new_grid[i, j] = 0
    return new_grid

# Create the animation
fig = plt.figure()
im = plt.imshow(grid, cmap='gray', animated=True)
def animate(*args):
    global grid
    grid = update(grid)
    im.set_array(grid)
    return im,
ani = animation.FuncAnimation(fig, animate, interval=500, blit=True)
plt.show()
'''