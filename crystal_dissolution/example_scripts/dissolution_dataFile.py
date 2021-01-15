import numpy as np
import copy
import os

from setup.dissolution import findNeighbors, removeVoxels

# ====== LOAD DATA FILE ======

# Select file
filename = 'CALSPAR1C_init_crystal_165x60x190_sub10.raw'

# Size of system
width = 165; height = 60; depth = 190; 
gridSize = max(width, height, depth)

# Size of grid
x,y,z = np.indices((depth, height, width))

# Read binary file
fileID = open(filename, "rb")
voxels = np.fromfile(fileID, dtype=np.uint8).reshape(depth, height, width)

fileID.close()


# ====== REMOVAL RATES ======

rmCorners = 1.00
rmEdges = 0.05
rmTerraces = 0.0
rmBulk = 0.0


# ====== RUN SIMULATION ======

# Empty arrays
removeCorners = []; removeEdges = []; removeTerraces = []; removeBulk = []
sumCorners = [];    sumEdges = [];    sumTerraces = [];  sumBulk = []; totalVoxels = []

# Make folder for binary files
if not os.path.exists("binaries"):
    os.makedirs("binaries")

# Time iterations
time = 3

for t in range(1, time+1):
    print("Starting iteration no. %d" %t)

    # Find number of neighbors
    corners, edges, terraces, bulk = findNeighbors(voxels, sumCorners, sumEdges, sumTerraces, sumBulk, totalVoxels)

    # Remove voxels (corners, edges, terraces)
    corners_bool, edges_bool, terraces_bool, bulk_bool = removeVoxels(corners, edges, terraces, bulk, rmCorners, rmEdges, rmTerraces, rmBulk, removeCorners, removeEdges, removeTerraces, removeBulk)
    
    # Put together to one array (voxels)
    voxels = np.asarray(corners_bool | edges_bool | terraces_bool | bulk_bool, dtype=np.int8)

    # Save iteration as binary-file
    output = open("binaries/output%03d.raw" % t, "wb")
    output.write(voxels)
    output.close()

    # Save output data
    np.savetxt('removedCorners.txt', removeCorners); np.savetxt('removedEdges.txt', removeEdges); np.savetxt('removedTerraces.txt', removeTerraces), np.savetxt('removedBulk.txt', removeBulk)
    np.savetxt('sumCorners.txt', sumCorners); np.savetxt('sumEdges.txt', sumEdges); np.savetxt('sumTerraces.txt', sumTerraces)

    # Break loop if there is only impurities left in the simulation
    if np.sum(voxels) == 0 or ((np.sum(corners) == 0 and np.sum(edges) == 0 and np.sum(terraces) == 0 and np.sum(bulk) == 0)):
        print('No more voxels in simulation')
        break
