import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import binary_erosion

# Read in binary files
fileID0 =  open("binaries/output000.bin", "rb")
fileID5 =  open("binaries/output005.bin", "rb")
fileID10 = open("binaries/output010.bin", "rb")
fileID15 = open("binaries/output015.bin", "rb")
fileID20 = open("binaries/output020.bin", "rb")
fileID30 = open("binaries/output030.bin", "rb")
fileID40 = open("binaries/output040.bin", "rb")
fileID50 = open("binaries/output050.bin", "rb")

# Size of files
width = 165; height = 60; depth = 190; 

# Save data files in array and reshape to correct size
data_0  = np.fromfile(fileID0,  dtype=np.uint8).reshape(depth, height, width)
data_5  = np.fromfile(fileID5,  dtype=np.uint8).reshape(depth, height, width)
data_10 = np.fromfile(fileID10, dtype=np.uint8).reshape(depth, height, width)
data_15 = np.fromfile(fileID15, dtype=np.uint8).reshape(depth, height, width)
data_20 = np.fromfile(fileID20, dtype=np.uint8).reshape(depth, height, width)
data_30 = np.fromfile(fileID30, dtype=np.uint8).reshape(depth, height, width)
data_40 = np.fromfile(fileID40, dtype=np.uint8).reshape(depth, height, width)
data_50 = np.fromfile(fileID50, dtype=np.uint8).reshape(depth, height, width)

# Make empty arrays to save sliced data in
sliced0  = np.zeros((data_0.shape[0], data_0.shape[1]), dtype=np.uint8)
sliced5  = np.zeros((data_0.shape[0], data_0.shape[1]), dtype=np.uint8)
sliced10 = np.zeros((data_0.shape[0], data_0.shape[1]), dtype=np.uint8)
sliced15 = np.zeros((data_0.shape[0], data_0.shape[1]), dtype=np.uint8)
sliced20 = np.zeros((data_0.shape[0], data_0.shape[1]), dtype=np.uint8)
sliced30 = np.zeros((data_0.shape[0], data_0.shape[1]), dtype=np.uint8)
sliced40 = np.zeros((data_0.shape[0], data_0.shape[1]), dtype=np.uint8)
sliced50 = np.zeros((data_0.shape[0], data_0.shape[1]), dtype=np.uint8)

# Loop through data set and retreive selected data to make a 2D slice
for i in range(0, data_0.shape[0]):
    for j in range(0, data_0.shape[1]):
        for k in range(0, data_0.shape[2]):

            if k == np.round(165/2):
                if data_0[i,j,k] == 1:
                    sliced0[i,j] = 1
                if data_5[i,j,k] == 1:
                    sliced5[i,j] = 1
                if data_10[i,j,k] == 1:
                    sliced10[i,j] = 1
                if data_15[i,j,k] == 1:
                    sliced15[i,j] = 1
                if data_20[i,j,k] == 1:
                    sliced20[i,j] = 1
                if data_30[i,j,k] == 1:
                    sliced30[i,j] = 1 
                if data_40[i,j,k] == 1:
                    sliced40[i,j] = 1
                if data_50[i,j,k] == 1:
                    sliced50[i,j] = 1


# Calculate amount of erosion
calculate_erosion5  = binary_erosion(sliced5)
calculate_erosion10 = binary_erosion(sliced10)
calculate_erosion15 = binary_erosion(sliced15)
calculate_erosion20 = binary_erosion(sliced20)
calculate_erosion30 = binary_erosion(sliced30)
calculate_erosion40 = binary_erosion(sliced40)
calculate_erosion50 = binary_erosion(sliced50)

# Find difference between binary image and amount of erosion
erosion5  = sliced5-calculate_erosion5
erosion10 = sliced10-calculate_erosion10
erosion15 = sliced15-calculate_erosion15
erosion20 = sliced20-calculate_erosion20
erosion30 = sliced30-calculate_erosion30
erosion40 = sliced40-calculate_erosion40
erosion50 = sliced50-calculate_erosion50


# Calculate distance map at t0 (cv2.DIS_L2 uses Euclidean distnace transformations)
distmap0 = cv2.distanceTransform(sliced0, cv2.DIST_L2, cv2.DIST_MASK_5)

# Find retreat around the crystal during deltaT=ti-t0
delta5to0  = distmap0*erosion5
delta10to0 = distmap0*erosion10
delta15to0 = distmap0*erosion15
delta20to0 = distmap0*erosion20
delta30to0 = distmap0*erosion30
delta40to0 = distmap0*erosion40
delta50to0 = distmap0*erosion50


# Plot distance maps
fig1 = plt.figure(1)
fig1.suptitle('Distance maps. Middle of the crystal', fontSize=16)
plt.subplot(2,4,1)
plt.title('t0')
plt.imshow(distmap0, cmap='plasma')
plt.colorbar()
plt.subplot(2,4,2)
plt.title('t5-t0')
plt.imshow(delta5to0, cmap='plasma')#, vmin=0, vmax=12)
plt.colorbar()
plt.subplot(2,4,3)
plt.title('t10-t0')
plt.imshow(delta10to0, cmap='plasma')#, vmin=0, vmax=12)
plt.colorbar()
plt.subplot(2,4,4)
plt.title('t15-t0')
plt.imshow(delta15to0, cmap='plasma')#, vmin=0, vmax=12)
plt.colorbar()
plt.subplot(2,4,5)
plt.title('t20-t0')
plt.imshow(delta20to0, cmap='plasma')#, vmin=0, vmax=12)
plt.colorbar()
plt.subplot(2,4,6)
plt.title('t30-t0')
plt.imshow(delta30to0, cmap='plasma')#, vmin=0, vmax=12)
plt.colorbar()
plt.subplot(2,4,7)
plt.title('t40-t0')
plt.imshow(delta40to0, cmap='plasma')#, vmin=0, vmax=12)
plt.colorbar()
plt.subplot(2,4,8)
plt.title('t50-t0')
plt.imshow(delta50to0, cmap='plasma')#, vmin=0, vmax=12)
plt.colorbar()


# Plot crystal evolution
fig2 = plt.figure(2)
fig2.suptitle('Crystal evolution', fontSize=16)
plt.subplot(2,4,1)
plt.title('t0')
plt.imshow(sliced0, cmap='RdPu', vmin=0, vmax=1)
plt.subplot(2,4,2)
plt.title('t5')
plt.imshow(sliced5, cmap='RdPu', vmin=0, vmax=1)
plt.subplot(2,4,3)
plt.title('t10')
plt.imshow(sliced10, cmap='RdPu', vmin=0, vmax=1)
plt.subplot(2,4,4)
plt.title('t15')
plt.imshow(sliced15, cmap='RdPu', vmin=0, vmax=1)
plt.subplot(2,4,5)
plt.title('t20')
plt.imshow(sliced20, cmap='RdPu', vmin=0, vmax=1)
plt.subplot(2,4,6)
plt.title('t30')
plt.imshow(sliced30, cmap='RdPu', vmin=0, vmax=1)
plt.subplot(2,4,7)
plt.title('t40')
plt.imshow(sliced40, cmap='RdPu', vmin=0, vmax=1)
plt.subplot(2,4,8)
plt.title('t50')
plt.imshow(sliced50, cmap='RdPu', vmin=0, vmax=1)

plt.tight_layout()
plt.show()
