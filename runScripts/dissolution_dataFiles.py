import numpy as np
import matplotlib.pyplot as plt
import copy
import os

from setup.makeSystem import makeClusters, createDislocation
from setup.dissolution import findNeighbors, removeVoxels
from setup.convenience import *


# ====== INPUT PARAMETERS ======

# Size of system
width = 165; height = 60; depth = 190; 
gridSize = max(width, height, depth)

# Select file
filename = 'CALSPAR1C_init_crystal_165x60x190_sub10.raw'

# % of Corners, Edges and Terraces to be removed
rmCorners = 1.00
rmEdges = 0.50
rmTerraces = 0.0
rmBulk = 0.0

# % impurity elements
percentImpurity = 0.00
minCluster = 0
maxCluster = 0

# Size of dislocation
dislocationHeight = 0
dislocationDepth  = 0

# Number of timesteps
timesteps = 15


# ====== MAKE SYSTEM ======

# Size of grid
x,y,z = np.indices((depth, height, width))

# Read binary file
fileID = open(filename, "rb")
data = np.fromfile(fileID, dtype=np.uint8).reshape(depth, height, width)

voxels = np.array(data, dtype = bool)

# Make impurities clusters
impurities = makeClusters(percentImpurity, voxels, height, depth, width, minCluster, maxCluster)

# Make dislocations
dislocations = createDislocation(voxels, dislocationHeight, dislocationDepth, depth)

# Empty arrays
removeCorners = []; removeEdges = []; removeTerraces = []; removeImpurities = []; removeBulk = []
sumCorners = [];    sumEdges = [];    sumTerraces = [];    sumImpurities = []; sumBulk = []; totalVoxels = []

# Make folders for images and binary files
if not os.path.exists(images):
    os.makedirs(images)


# ====== RUN SIMULATION ======

# Initial setup
corners, edges, terraces, bulk = emptyMatrixes(x,y,z)
corners, edges, terraces, bulk, impurities, dislocations = findNeighbors(voxels, impurities, corners, edges, terraces, bulk, dislocations, sumCorners, sumEdges, sumTerraces, sumImpurities, sumBulk, totalVoxels)
corners_bool, edges_bool, terraces_bool, bulk_bool, impurities_bool, dislocations_bool = convertToBoolean(corners, edges, terraces, bulk, impurities, dislocations)

voxels = corners_bool | edges_bool | terraces_bool | bulk_bool | impurities_bool | dislocations_bool

colors = setColors(voxels, corners_bool, edges_bool, terraces_bool, bulk_bool, impurities_bool, dislocations_bool)

plotFigure(voxels, gridSize, colors)
plt.savefig('images/plot000.png', dpi=300)
plt.close()

output = open("binaries/output000.bin", "wb")
output.write(voxels)
output.close()

# Start loop

time = timesteps

for t in range(1,time+1):
    print(t)

    # Remove voxels (corners, edges, terraces)
    corners, edges, terraces, bulk = removeVoxels(corners, edges, terraces, bulk, rmCorners, rmEdges, rmTerraces, rmBulk, removeCorners, removeEdges, removeTerraces, removeBulk)
    corners_bool, edges_bool, terraces_bool, bulk_bool, impurities_bool, dislocations_bool = convertToBoolean(corners, edges, terraces, bulk, impurities, dislocations)
    
    voxels = corners_bool | edges_bool | terraces_bool | bulk_bool | dislocations_bool


    # Find neighbors of the new dataset
    corners, edges, terraces, bulk = emptyMatrixes(x,y,z)
    corners, edges, terraces, bulk, impurities, dislocations = findNeighbors(voxels, impurities, corners, edges, terraces, bulk, dislocations, sumCorners, sumEdges, sumTerraces, sumImpurities, sumBulk, totalVoxels)
    corners_bool, edges_bool, terraces_bool, bulk_bool, impurities_bool, dislocations_bool = convertToBoolean(corners, edges, terraces, bulk, impurities, dislocations)

    voxels = corners_bool | edges_bool | terraces_bool | bulk_bool | impurities_bool | dislocations_bool

    colors = setColors(voxels, corners_bool, edges_bool, terraces_bool, bulk_bool, impurities_bool, dislocations_bool)


    # Plot current step and save as figure
    plotFigure(voxels, gridSize, colors)

    if t < 10:
        plt.savefig('images/plot00'+str(t)+'.png', dpi=300)
        output = open('binaries/output00'+str(t)+'.bin', "wb")
        output.write(voxels)
        output.close()
    if t > 9 and t < 100:
        plt.savefig('images/plot0'+str(t)+'.png', dpi=300)
        output = open('binaries/output0'+str(t)+'.bin', "wb")
        output.write(voxels)
        output.close()
    if t > 99:
        plt.savefig('images/plot'+str(t)+'.png', dpi=300)
        output = open('binaries/output0'+str(t)+'.bin', "wb")
        output.write(voxels)
        output.close()

    plt.close()


    # Save output data
    np.savetxt('removedCorners.txt', removeCorners); np.savetxt('removedEdges.txt', removeEdges); np.savetxt('removedTerraces.txt', removeTerraces)
    np.savetxt('removedImpurities.txt', removeImpurities); np.savetxt('removedBulk.txt', removeBulk)

    np.savetxt('sumCorners.txt', sumCorners); np.savetxt('sumEdges.txt', sumEdges); np.savetxt('sumTerraces.txt', sumTerraces)


    # Break loop if there is only impurities left in the simulation
    if np.sum(voxels) == 0 or (np.sum(corners) == 0 and np.sum(edges) == 0 and np.sum(terraces) == 0 and np.sum(bulk) == 0):
        break


# ====== MAKE IMAGES FROM SIMULATION INTO GIF ======
makeGIF()
