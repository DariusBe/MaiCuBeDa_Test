import cv2
from matplotlib.widgets import Slider
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from Utils import xyzFileToImg, Vec2D, pos_to_grid, blurMap
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
        self.sensor_map = np.zeros((grid_size, grid_size))
        self.penalty_map = xyzFileToImg(filepath, self.grid_size, 3)
        self.oat_map = self.createOatMap()
        self.population = []

    # if no file is given, create a blank grid
    def createOatMap(self):
        oatMap = np.zeros((self.grid_size, self.grid_size))
        # create a few circles with random radius and position
        for i in range(3):
            radius = np.random.randint(4, 8)
            x = np.random.randint(self.grid_size//2, self.grid_size)
            y = np.random.randint(0, self.grid_size)
            cv2.circle(oatMap, (x, y), radius, 5, -1)
        return oatMap*6

    def populate(self):
        population = []
        for i in range(self.physarus_count):
            rand_x = self.grid_size // 2 + np.random.uniform(-self.grid_size // 50, self.grid_size // 50)
            rand_y = self.grid_size // 2 + np.random.uniform(-self.grid_size // 50, self.grid_size // 50)
            rand_heading = np.random.choice([-self.rotation_angle, self.rotation_angle])
            # def __init__(self, position, heading, sensor_distance, sensor_width, sensor_angle):
            population.append(Physarum(Vec2D(rand_x, rand_y), rand_heading, self.sensor_distance, self.sensor_width, self.sensor_angle))
        self.population = population

    def attemptMove(self, grid):
        # Loop over all cells in the grid and place one Physarum
        for physarum in self.population:
            # Get the position of the Physarum in the grid
            pos_x, pos_y = pos_to_grid(physarum.position, self.grid_size)
            grid[pos_x, pos_y] = 1

            # attempt to move
            if physarum.can_move(self.trail, physarum.position, self.step_width):
                physarum.move(self.step_width, self.grid_size)
                physarum.rotate(self.rotation_angle)
                pos_x, pos_y = pos_to_grid(physarum.position, self.grid_size)
                self.trail[pos_x, pos_y] = 1
            else:
                rand_heading = np.random.choice([-self.rotation_angle, self.rotation_angle])
                #rand_heading = np.random.choice(np.arange(0, 360, self.rotation_angle))
                physarum.heading = rand_heading
        return grid

    def senseAndConquer(self):
        for physarum in self.population:
            self.sensor_map = np.zeros((self.grid_size, self.grid_size))
            self.sensor_map = physarum.showSensorPositions(self.sensor_map)
            sensor_values = physarum.sense(self.trail + self.oat_map)
            physarum.attraction_rules(self.step_width, self.grid_size, sensor_values)

    def update(self, old_grid):
        grid = old_grid.copy()
        # shuffle population
        np.random.shuffle(self.population)
        # Loop over all cells in the grid and place one Physarum
        grid = self.attemptMove(grid)
        np.random.shuffle(self.population)
        self.senseAndConquer()
        return grid
    
    def runSimulation(self, interval):
        self.grid[self.grid_size//2, self.grid_size//2] = 1
        self.populate()

        fig, ax = plt.subplots()
        ax.set_xlim(0, self.grid_size)
        ax.set_ylim(0, self.grid_size)
        # stack the images
        #im1 = ax.imshow(self.oat_map, cmap='gray', origin='lower')
        #m2 = ax.imshow(self.trail, cmap='gray', origin='lower')
        im = ax.imshow(self.trail, cmap='cividis', origin='lower')

        # create sliders
        decay_slider = Slider(plt.axes([0.5, 0.01, 0.25, 0.02]), 'Penalty Decay Rate', 0.5, 1.0, valinit=self.trail_decay)
        rotation_angle_slider = Slider(plt.axes([0.5, 0.04, 0.25, 0.02]), 'Rotation Angle', 0, 180, valinit=self.rotation_angle)
        step_width_slider = Slider(plt.axes([0.5, 0.07, 0.25, 0.02]), 'Step Width', 0.5, 5, valinit=self.step_width)
        sensor_distance_slider = Slider(plt.axes([0.5, 0.10, 0.25, 0.02]), 'Sensor Distance', 5, 20, valinit=self.sensor_distance)
        sensor_angle_slider = Slider(plt.axes([0.5, 0.13, 0.25, 0.02]), 'Sensor Angle', 22.5, 90, valinit=self.sensor_angle)
        # make space for the sliders
        plt.subplots_adjust(left=0.1, bottom=0.2)


        def animate(*args):
            global grid
            self.trail_decay = decay_slider.val
            self.rotation_angle = rotation_angle_slider.val
            self.step_width = step_width_slider.val
            self.sensor_distance = sensor_distance_slider.val
            self.sensor_angle = sensor_angle_slider.val
            #self.oat_map -= (self.trail * 0.01)

            # diffuse the trail using cv2.dilate
            self.trail += self.oat_map
            self.trail = self.update(self.trail) * self.trail_decay
            im.set_array(self.trail)
            return im,

        ani = animation.FuncAnimation(fig, animate, cache_frame_data=False, interval=interval, blit=True)
        plt.colorbar(im)
        plt.show()

        


filepath = "Physarum/geo_data/dgm_33250-5889.xyz"
grid_size = 100
trail_decay = 0.9
population = 250
rotation_angle = 22.5
step_width = 1
sensor_distance = 10
sensor_angle = 45
sensor_width = 1

simulation = PhysarumSimulation(population, filepath, rotation_angle, sensor_distance, sensor_angle, sensor_width, step_width, grid_size, trail_decay)
simulation.runSimulation(1)