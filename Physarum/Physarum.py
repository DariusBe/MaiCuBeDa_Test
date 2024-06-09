import numpy as np
from Utils import Vec2D, pos_to_grid

class Physarum:
    def __init__(self, position, heading, sensor_distance, sensor_width, sensor_angle):
        self.position = position
        self.heading = heading
        self.sensor_distance = sensor_distance
        self.sensor_width = sensor_width
        self.sensor_angle = sensor_angle
        self.sensor_values = [
            # sensor 1 (forward = F)
            Vec2D(self.position.x + self.sensor_distance * np.cos(np.radians(self.heading)),
                self.position.y + self.sensor_distance * np.sin(np.radians(self.heading))), 
            # sensor 2 (left = FL)
            Vec2D(self.position.x + self.sensor_distance * np.cos(np.radians(self.heading + self.sensor_angle)),
                self.position.y + self.sensor_distance * np.sin(np.radians(self.heading + self.sensor_angle))),
            # sensor 3 (right = FR)
            Vec2D(self.position.x + self.sensor_distance * np.cos(np.radians(self.heading - self.sensor_angle)),
                self.position.y + self.sensor_distance * np.sin(np.radians(self.heading - self.sensor_angle)))
        ]

    def sense(self, grid):
        sensor_values = []
        for sensor in self.sensor_values:
            # update current position of the sensor
            sensor.x = self.position.x + self.sensor_distance * np.cos(np.radians(self.heading))
            sensor.y = self.position.y + self.sensor_distance * np.sin(np.radians(self.heading))
            pos_x, pos_y = pos_to_grid(sensor, len(grid))
            sensor_values.append(grid[pos_x, pos_y])
        return sensor_values

    def rotate(self, rotation_angle):
        # randomly around +/- rotation_angle
        self.heading += np.random.choice([-rotation_angle, rotation_angle])
    
    def move(self, step_width, grid_size):
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
    def can_move(self, grid, position, step_width):
        # check if at future position, there is aleady a Physarum
        future_pos = Vec2D(position.x + step_width * np.cos(np.radians(self.heading)), position.y + step_width * np.sin(np.radians(self.heading)))
        pos_x, pos_y = pos_to_grid(future_pos, len(grid))
        # if future position is inside the grid, get 
        if pos_x < 0 or pos_x >= len(grid) or pos_y < 0 or pos_y >= len(grid):
            return False
        return True