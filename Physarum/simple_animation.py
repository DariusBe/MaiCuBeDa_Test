from matplotlib.widgets import Slider
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# global variables:
grid_size = 250
trail_decay = 0.9
step_width = 1.0
rotation_angle = 22.5
sensor_angles = 45.0
sensor_distances = 9.0


# define numpy 2D Vector
class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Physarum:
    def __init__(self, position, heading):
        self.position = position
        self.heading = heading

    def rotate(self, rotation_angle):
        # randomly around +/- rotation_angle
        self.heading += np.random.uniform(-rotation_angle, rotation_angle)
    
    def move(self,step_width):
        self.position.x += step_width * np.cos(np.radians(self.heading))
        self.position.y += step_width * np.sin(np.radians(self.heading))



# map position to grid
def pos_to_grid(pos):
    return int(pos.x), int(pos.y)

grid = np.zeros((grid_size, grid_size))
grid[grid_size//2, grid_size//2] = 0.000001

# initialize the grid with some low values
trail = np.random.normal(-0.25, 0.25, size=(grid_size, grid_size))
# cut off the negative values
trail = np.clip(trail, 0, 1)

particles = []
for i in range(1):
    particles.append(Physarum(Vec2D(np.random.normal(scale=grid_size), np.random.normal(scale=grid_size)), np.random.randint(0, 360)))

def update(last_grid, rotation_angle=rotation_angle, step_width=step_width):
    grid = last_grid.copy()
    # Loop over all cells in the grid and place one Physarum
    for physarum in particles:
        physarum.position.x = physarum.position.x % grid_size
        physarum.position.y = physarum.position.y % grid_size
        # Get the position of the Physarum in the grid
        pos_x, pos_y = pos_to_grid(physarum.position)
        grid[pos_x, pos_y] = 1
        
        physarum.rotate(rotation_angle)
        physarum.move(step_width)
    return grid



fig = plt.figure()
im = plt.imshow(grid, cmap='terrain', animated=True)
speed_slider = Slider(plt.axes([0.1, 0.01, 0.8, 0.03]), 'Physarum Step Width', 0.001, 10.0, valinit=step_width)
rotation_slider = Slider(plt.axes([0.1, 0.05, 0.8, 0.03]), 'Physarum Rotation Angle', 0, 90, valinit=rotation_angle)
def animate(*args):
    global grid
    global step_width
    global rotation_angle
    step_width = speed_slider.val
    rotation_angle = rotation_slider.val
    grid = update(grid, rotation_angle, step_width)
    im.set_array(grid)
    return im,
ani = animation.FuncAnimation(fig, animate, interval=5, blit=True)
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