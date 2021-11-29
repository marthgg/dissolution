import numpy as np
from scipy.ndimage import binary_erosion
from scipy import ndimage
import os

# Make folder for retreat files
if not os.path.exists("retreat"):
    os.makedirs("retreat")

# Size of file
width = 1650; height = 600; depth = 1900

# Initial binary file
fileID_initial = open('CALSPAR1C_init_crystal_rotated40_1650x600x1900.raw', "rb")
data_initial  = np.fromfile(fileID_initial,  dtype=np.uint8).reshape(depth, height, width)

fileID_step = open('binaries/output045.raw', "rb")
data_step  = np.fromfile(fileID_step,  dtype=np.uint8).reshape(depth, height, width)

# Calculate amount of erosion
calculate_erosion_step  = binary_erosion(data_step)

# Find difference between binary image and amount of erosion
erosion_step  = data_step-calculate_erosion_step

# Calculate distance map at t0
distmap_initial = ndimage.distance_transform_edt(data_initial)

# Find retreat around the crystal during deltaT=ti-t0
retreat = distmap_initial*erosion_step

# Save as binary-file
crystal_distmap = np.asarray(retreat, dtype=np.int8)
output = open("retreat/retreat_crystal045.raw", "wb")
output.write(crystal_distmap)
output.close()

# Save as txt-file
dissolution_rate = retreat[retreat != 0]
np.savetxt('retreat/retreat_crystal045.txt', dissolution_rate)
