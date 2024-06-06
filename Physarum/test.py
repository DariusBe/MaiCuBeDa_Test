import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2


# Initialize grid
gridsize = 100
grid = np.zeros((gridsize, gridsize))

# define a class particle with position and heading both as 2d-vectors
class Particle:
    def __init__(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading

# create a list of randomly placed particles
particles = []
population = 100 
for i in range(population):
    particles.append(Particle(np.random.rand(), np.random.rand(), np.random.rand(2)))


# map positions from range 0-1 to gridsize
def map_to_grid(x, y):
    x = int(x * gridsize)
    y = int(y * gridsize)
    return x, y

# define circle primitive to display particles
def circle(x, y, r):
    t = np.linspace(0, 2*np.pi, 100)
    return x + r*np.cos(t), y + r*np.sin(t)

# fill pixels of a circle on the grid
def plot_circles(ax, x, y, r):
    for i in range(len(x)):
        t = np.linspace(0, 2*np.pi, 100)
        ax.fill(x[i] + r*np.cos(t), y[i] + r*np.sin(t), 'b')

def prep(grid, particles):
    last = np.zeros((gridsize, gridsize))
    for p in particles:
        # map particle position to grid
        p.x, p.y = map_to_grid(p.x, p.y)
        plot_circles(plt, [p.x], [p.y], 1)
        # turn plot into image
    plt.axis('off')
    plt.savefig('test.png')
    # read image
    img = cv2.imread('test.png', cv2.IMREAD_GRAYSCALE)
    plt.imshow(img, cmap='gray')
    plt.show()

prep(grid, particles)

