import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Initialize grid
grid = np.random.choice([0, 1], size=(50, 50))

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
                # If it has 4 or more neighbors, fill the cell
                if np.sum(neighbors) >= 4:
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
ani = animation.FuncAnimation(fig, animate, interval=100, blit=True)
plt.show()