import cv2
from matplotlib.widgets import Slider
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from Utils import xyzFileToImg, Vec2D, pos_to_grid
from Physarum import Physarum

class PhysarumSimulation:
    def __init__(self, physarus_count=100, filepath="", rotation_angle = 22.5, sensor_distance=9, sensor_angle=22.5, sensor_width=1, step_width=1, grid_size=500,  trail_decay=0.9):
        self.physarus_count = physarus_count
        self.filepath = filepath
        self.rotation_angle = rotation_angle
        self.step_width = step_width
        self.grid_size = grid_size
        self.trail_decay = trail_decay
        self.sensor_distance = sensor_distance
        self.sensor_angle = sensor_angle
        self.sensor_width = sensor_width
        self.grid = np.zeros((grid_size, grid_size))
        self.trail = np.zeros((grid_size, grid_size))
        self.penalty_map = xyzFileToImg(filepath, self.grid_size)
        self.population = []

    def populate(self):
        population = []
        for i in range(self.physarus_count):
            rand_x = self.grid_size // 2 + np.random.uniform(-self.grid_size // 50, self.grid_size // 50)
            rand_y = self.grid_size // 2 + np.random.uniform(-self.grid_size // 50, self.grid_size // 50)
            rand_heading = np.random.choice(np.arange(0, 360, self.rotation_angle))
            # def __init__(self, position, heading, sensor_distance, sensor_width, sensor_angle):
            population.append(Physarum(Vec2D(rand_x, rand_y), rand_heading, self.sensor_distance, self.sensor_width, self.sensor_angle))
        self.population = population



    def update(self, old_grid):
        grid = old_grid.copy()
        # Loop over all cells in the grid and place one Physarum
        for physarum in self.population:
            # Get the position of the Physarum in the grid
            pos_x, pos_y = pos_to_grid(physarum.position, self.grid_size)
            #grid[pos_x-2:pos_x+2, pos_y-2:pos_y+2] = 0.25
            grid[pos_x, pos_y] = 1

            # attempt to move
            if physarum.can_move(self.grid, physarum.position, self.step_width):
                physarum.move(self.step_width, self.grid_size)
                physarum.rotate(self.rotation_angle)
                # leave trail
                self.trail[pos_x, pos_y] = 1
            else:
                rand_heading = np.random.choice(np.arange(0, 360, self.rotation_angle))
                physarum.heading = rand_heading

            # sense
            sensor_values = physarum.sense(self.penalty_map)
            print(sensor_values)

        return grid
    
    def runSimulation(self, interval):
        self.grid[self.grid_size//2, self.grid_size//2] = 1
        self.populate()

        fig, ax = plt.subplots()
        ax.set_xlim(0, self.grid_size)
        ax.set_ylim(0, self.grid_size)
        im = ax.imshow(self.grid, cmap='cividis', origin='lower')

        decay_slider = Slider(plt.axes([0.5, 0.01, 0.25, 0.02]), 'Penalty Decay Rate', 0.5, 1.0, valinit=self.trail_decay)


        def animate(*args):
            global grid
            global rotation_angle
            trail_decay = decay_slider.val
            self.trail = self.update(self.trail) * trail_decay
            im.set_array(self.trail + self.penalty_map)
            return im,

        ani = animation.FuncAnimation(fig, animate, interval=interval)
        plt.colorbar(im)
        plt.show()

        


filepath = "Physarum/geo_data/dgm_33250-5889.xyz"
grid_size = 50
trail_decay = 0.95
population = 1
rotation_angle = 22.5
step_width = 1.0
sensor_distance = 9
sensor_angle = 22.5
sensor_width = 1

simulation = PhysarumSimulation(population, filepath, rotation_angle, sensor_distance, sensor_angle, sensor_width, step_width, grid_size, trail_decay)
simulation.runSimulation(100)