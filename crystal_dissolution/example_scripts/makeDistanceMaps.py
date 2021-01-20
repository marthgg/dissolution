import numpy as np
from scipy.ndimage import binary_erosion
from scipy import ndimage

from mayavi import mlab

# Read in binary files
fileID0  = open("CALSPAR1C_init_crystal_165x60x190_sub10.raw", "rb")
fileID3  = open("binaries/output003.raw", "rb")
fileID6  = open("binaries/output006.raw", "rb")
fileID9  = open("binaries/output009.raw", "rb")
fileID12 = open("binaries/output012.raw", "rb")
fileID20 = open("binaries/output020.raw", "rb")

# Size of files
width = 165; height = 60; depth = 190; 

# Save data files in array and reshape to correct size
data_0  = np.fromfile(fileID0,  dtype=np.uint8).reshape(depth, height, width)
data_3  = np.fromfile(fileID3,  dtype=np.uint8).reshape(depth, height, width)
data_6  = np.fromfile(fileID6,  dtype=np.uint8).reshape(depth, height, width)
data_9  = np.fromfile(fileID9,  dtype=np.uint8).reshape(depth, height, width)
data_12 = np.fromfile(fileID12, dtype=np.uint8).reshape(depth, height, width)
data_20 = np.fromfile(fileID20, dtype=np.uint8).reshape(depth, height, width)

# Calculate amount of erosion
calculate_erosion3  = binary_erosion(data_3)
calculate_erosion6  = binary_erosion(data_6)
calculate_erosion9  = binary_erosion(data_9)
calculate_erosion12 = binary_erosion(data_12)
calculate_erosion20 = binary_erosion(data_20)

# Find difference between binary image and amount of erosion
erosion2  = data_3-calculate_erosion3
erosion6  = data_6-calculate_erosion6
erosion8  = data_9-calculate_erosion9
erosion12 = data_12-calculate_erosion12
erosion20 = data_20-calculate_erosion20

# Calculate distance map at t0
distmap0 = ndimage.distance_transform_edt(data_0)

# Find retreat around the crystal during deltaT=ti-t0
delta3to0  = distmap0*erosion2
delta6to0  = distmap0*erosion6
delta9to0  = distmap0*erosion8
delta12to0 = distmap0*erosion12
delta20to0 = distmap0*erosion20

delta20to0 = np.asarray(delta20to0, dtype=np.float64)

# Plot using mayavi
mlab.points3d(delta20to0, mode="cube", colormap='jet', scale_factor=1)
mlab.colorbar(orientation='vertical')

mlab.show()