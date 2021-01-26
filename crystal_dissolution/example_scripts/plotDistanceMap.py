import numpy as np
from analyse.distanceMap import createFileForDistanceMap
from mayavi import mlab
# from scipy.ndimage import binary_erosion
# from scipy import ndimage

# Read in binary files
fileID_initial = open("CALSPAR1C_init_crystal_165x60x190_sub10.raw", "rb")
fileID_step  = open("binaries/output020.raw", "rb")

# Size of files
width = 165; height = 60; depth = 190

# Output filename
outputfilename = 'fileName.txt'

# Make text files
createFileForDistanceMap(fileID_initial, fileID_step, width, depth, height, outputfilename)


# Read file from disk to plot
new_data = np.loadtxt(outputfilename)

# Make it a 3D-array
new_data = new_data.reshape((depth, height, width))

# Plot using mayavi
mlab.points3d(new_data, mode="cube", colormap='jet', scale_factor=1)
mlab.colorbar(orientation='vertical')

mlab.show()