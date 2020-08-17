import numpy as np
import matplotlib.pyplot as plt
import copy

from setup.makeSystem import makeClusters, createDislocation
from setup.dissolution import findNeighbors, removeVoxels
from setup.convenience import *


# ====== INPUT PARAMETERS ======

# Size of system
height = 52; depth = 52; width = 52
gridSize = max(height, width, depth)

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
dislocationWidth = width*10
dislocationDepth = 3



# ====== MAKE SYSTEM ======

# Size of grid
x,y,z = np.indices((height, depth, width))

# Create system
voxels = (x >= 1) & (x < height-1) & (y >= 1) & (y < depth-1) & (z >= 1) & (z < width-1)
voxels = np.array(voxels, dtype='uint8')   # Make it an int array

# Make impurities clusters
impurities = makeClusters(percentImpurity, voxels, height, depth, width, minCluster, maxCluster)

# Make dislocations
dislocations = createDislocation(voxels, dislocationWidth, dislocationDepth, depth)

# Empty arrays
removeCorners = []; removeEdges = []; removeTerraces = []; removeImpurities = []; removeBulk = []
sumCorners = [];    sumEdges = [];    sumTerraces = [];    sumImpurities = []; sumBulk = []; totalVoxels = []


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


# Start loop

time = 500

for t in range(1,time+1):
    print(t)

    # Remove voxels (corners, edges, terraces)
    corners, edges, terraces, bulk = removeVoxels(corners, edges, terraces, bulk, rmCorners, rmEdges, rmTerraces, rmBulk, removeCorners, removeEdges, removeTerraces, removeBulk)
    corners_bool, edges_bool, terraces_bool, bulk_bool, impurities_bool, dislocations_bool = convertToBoolean(corners, edges, terraces, bulk, impurities, dislocations)
    
    voxels = corners_bool | edges_bool | terraces_bool | bulk_bool | impurities_bool | dislocations_bool


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
    if t > 9 and t < 100:
        plt.savefig('images/plot0'+str(t)+'.png', dpi=300)
    if t > 99:
        plt.savefig('images/plot'+str(t)+'.png', dpi=300)

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