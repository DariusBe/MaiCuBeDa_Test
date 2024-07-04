import cv2
import numpy as np
import matplotlib.pyplot as plt


filepath = "geo_data/dgm_33250-5888.xyz"

# read the XYZ point cloud as heightmap
topo = np.loadtxt(filepath, delimiter=',')
# get the x and y coordinates
x = topo[:,0]
y = topo[:,1]
# get the z coordinates
z = topo[:,2]

# get the number of columns
nr_cols = len(np.unique(x))
# get the number of rows
nr_rows = len(np.unique(y))
# reshape the z coordinates
z = z.reshape(nr_cols, nr_rows)
# get the x and y coordinates
x = x[:nr_cols]
y = y[::nr_rows]


# # plot the topography
# plt.figure()
# plt.imshow(z, cmap='gray', origin='lower')
# plt.colorbar()
# plt.show()


# calculate the gradient of the topography
dx, dy = np.gradient(z)
# calculate the magnitude of the gradient
mag = np.sqrt(dx**2 + dy**2)
# normalize the gradient
mag = (mag - mag.min()) / (mag.max() - mag.min())


# # plot the gradient
# plt.figure()
# plt.imshow(mag, cmap='terrain', origin='lower')
# plt.colorbar()
# plt.show()


# save normalized gradient as a heightmap (0-255)
plt.imsave(filepath.split('.')[0] + '_gradient.png', mag, cmap='gray')

def xyzFileToImg(filepath, grid_size, factor=1.0):
    topo = np.loadtxt(filepath, delimiter=',')
    # get the x and y coordinates
    x = topo[:,0] # means all rows, only the first column
    y = topo[:,1] #                  --//-- second column
    z = topo[:,2] #                   --//-- third column
    # get the number of columns
    nr_cols = len(np.unique(x))
    nr_rows = len(np.unique(y))
    z = z.reshape(nr_cols, nr_rows)
    # calculate the gradient of the topography
    dx, dy = np.gradient(z)
    # calculate the magnitude of the gradient
    mag = np.sqrt(dx**2 + dy**2) # means sqrt(dx^2 + dy^2)
    # normalize the gradient
    norm = (mag - mag.min()) / (mag.max() - mag.min())
    # create trail map from normalized gradient
    penalty = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            penalty[i, j] = norm[int(i * nr_cols / grid_size), int(j * nr_rows / grid_size)]
    # corrode the penalty map
    penalty = cv2.GaussianBlur(penalty, (5, 5), 0)
    return penalty*factor

# define numpy 2D Vector
class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# map position to grid
def pos_to_grid(pos, grid_size=100):
    # make sure the position is within the grid
    pos.x = min(max(0, pos.x), grid_size - 1)
    pos.y = min(max(0, pos.y), grid_size - 1)
    return int(pos.x), int(pos.y)

# only lightly blur the penalty map using convolution
def blurMap(penalty_map, grid_size, scale_factor=1.0):
    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9 * scale_factor
    print(kernel.shape, kernel)
    blurred_map = cv2.filter2D(penalty_map, -1, kernel)
    return blurred_map

