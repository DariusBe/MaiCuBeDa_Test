from matplotlib.widgets import Slider
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# global variables:
grid_size = 350
trail_decay = 0.9
trail_factor = 1.0
step_width = 1.0
rotation_angle = 22.5
sensor_angles = 45.0
sensor_distances = 9.0
physarum_count = 250

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
    
    def move(self, step_width):
        self.position.x += step_width * np.cos(np.radians(self.heading))
        self.position.y += step_width * np.sin(np.radians(self.heading))
        # if position is outside the grid, set it to the edge of the grid
        self.position.x = min(max(0, self.position.x), grid_size - 1)
        self.position.y = min(max(0, self.position.y), grid_size - 1)
        # invert heading if position is at the edge of the grid
        if self.position.x in [0, grid_size - 1]:
            self.heading = 180 - self.heading
        if self.position.y in [0, grid_size - 1]:
            self.heading = -self.heading
    
    # is move possible?
    def can_move(self, position):
        # check if at future position, there is aleady a Physarum
        future_pos = Vec2D(position.x + step_width * np.cos(np.radians(self.heading)), position.y + step_width * np.sin(np.radians(self.heading)))
        future_pos = pos_to_grid(future_pos)
        if grid[future_pos] > 0:
            return False
        return True

grid = np.zeros((grid_size, grid_size))
grid[grid_size//2, grid_size//2] = 0.000000001 

# randomly create few spots with aggregated trail
trail = np.random.poisson(0.01, (grid_size, grid_size))
# randomize values > 0 in trail to values between 0.1 and 1.0
trail = np.where(trail > 0, np.random.uniform(0.1, 1.0, trail.shape), trail)

particles = []
for i in range(physarum_count):
    # spawn physarum from center of the grid
    rand_x = grid_size // 2 + np.random.uniform(-grid_size // 50, grid_size // 50)
    rand_y = grid_size // 2 + np.random.uniform(-grid_size // 50, grid_size // 50)

    rand_heading = np.random.choice(np.arange(0, 360, rotation_angle))
    
    particles.append(Physarum(Vec2D(rand_x, rand_y), rand_heading))

def update(last_grid, rotation_angle=rotation_angle, step_width=step_width):
    grid = last_grid.copy()
    # Loop over all cells in the grid and place one Physarum
    for physarum in particles:
        # Get the position of the Physarum in the grid
        pos_x, pos_y = pos_to_grid(physarum.position, grid_size)
        grid[pos_x, pos_y] = 1

        
        physarum.rotate(rotation_angle)
        if physarum.can_move(physarum.position):
            physarum.move(step_width)
        else:
            physarum.rotate(180)
            if physarum.can_move(physarum.position):
                physarum.move(step_width)
    return grid


fig = plt.figure()
# stack trail on top of the grid
im = plt.imshow(grid, cmap='cividis', animated=True)
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
    # multiply pixels by trail
    return im,
ani = animation.FuncAnimation(fig, animate, interval=1, blit=True)
# show colorbar
plt.colorbar(im)
plt.show()