import numpy as np
import matplotlib.pyplot as plt


filepath = "Physarum/geo_data/dgm_33250-5889.xyz"

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

'''
# plot the topography
plt.figure()
plt.imshow(z, cmap='terrain', origin='lower')
plt.colorbar()
plt.show()
'''

# calculate the gradient of the topography
dx, dy = np.gradient(z)
# calculate the magnitude of the gradient
mag = np.sqrt(dx**2 + dy**2)
# normalize the gradient
mag = (mag - mag.min()) / (mag.max() - mag.min())

'''
# plot the gradient
plt.figure()
plt.imshow(mag, cmap='gray', origin='lower')
plt.colorbar()
plt.show()
'''

# save normalized gradient as a heightmap (0-255)
plt.imsave(filepath.split('.')[0] + '_gradient.png', mag, cmap='gray')