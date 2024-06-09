import numpy as np
from Utils import Vec2D, pos_to_grid

class Physarum:
    def __init__(self, position, heading, sensor_distance, sensor_width, sensor_angle):
        self.position = position
        self.heading = heading
        self.sensor_distance = sensor_distance
        self.sensor_width = sensor_width
        self.sensor_angle = sensor_angle
        self.sensor_positions = [
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

    def updateSensorPositions(self):
        self.sensor_positions = [
            # sensor 1 (forward = F)
            Vec2D(self.position.x + self.sensor_distance * np.cos(np.radians(self.heading)),
                self.position.y + self.sensor_distance * np.sin(np.radians(self.heading))), 
            # sensor 2 (left = FL)
            Vec2D(self.position.x + self.sensor_distance * np.cos(np.radians(self.heading - self.sensor_angle)),
                self.position.y + self.sensor_distance * np.sin(np.radians(self.heading - self.sensor_angle))),
            # sensor 3 (right = FR)
            Vec2D(self.position.x + self.sensor_distance * np.cos(np.radians(self.heading + self.sensor_angle)),
                self.position.y + self.sensor_distance * np.sin(np.radians(self.heading + self.sensor_angle)))
        ]

    def sense(self, grid):
        sensor_values = []
        self.updateSensorPositions()
        for sensor_pos in self.sensor_positions:
            pos_x, pos_y = pos_to_grid(sensor_pos, len(grid))
            sensor_values.append(grid[pos_x, pos_y])
        return sensor_values

    def attraction_rules(self, step_width, grid_size, sensor_values):
        F, FL, FR = sensor_values[:3]
        # give rounded overview of the sensor values at the current position
        #print('F: {}, FL: {}, FR: {}'.format(round(sensor_values[0], 3), round(sensor_values[1], 3), round(sensor_values[2], 3)))
        if (F>FL) and (F>FR):
            # keep moving forward
            self.move(step_width, grid_size)
        elif (F<FL) and (F<FR):
            # rotate either +/-rotation_angle randomly
            rand_angle = np.random.choice([-self.sensor_angle, self.sensor_angle])
            self.heading += rand_angle
        elif (FL<FR):
            self.heading += self.sensor_angle
        elif (FR<FL):
            self.heading -= self.sensor_angle


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
    
    def showSensorPositions(self, grid):
        # show sensor positions on the grid
        for sensor_pos in self.sensor_positions:
            pos_x, pos_y = pos_to_grid(sensor_pos, len(grid))
            grid[pos_x, pos_y] = 1
        return grid