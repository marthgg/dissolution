import numpy as np
import os
from scipy.ndimage import convolve

def convertToBoolean(corners, edges, terraces, bulk):
    corners_bool = np.array(corners, dtype=bool)
    edges_bool = np.array(edges, dtype=bool)
    terraces_bool = np.array(terraces, dtype=bool)
    bulk_bool = np.array(bulk, dtype=bool)
    
    return corners_bool, edges_bool, terraces_bool, bulk_bool

def findNeighbors(voxels, sumCorners, sumEdges, sumTerraces, sumBulk, totalVoxels):
    counting_range = np.array([ [[0,0,0],[0,1,0],[0,0,0]], [[0,1,0],[1,0,1],[0,1,0]], [[0,0,0],[0,1,0],[0,0,0]] ])
    convolution = convolve(voxels, counting_range, mode="constant")

    corners = (convolution == 3) | (convolution == 2) | (convolution == 1)
    edges = (convolution == 4)
    terraces = (convolution == 5)
    bulk = (convolution == 6)

    corners = (corners & voxels)
    edges = (edges & voxels)
    terraces = (terraces & voxels)
    bulk = (bulk & voxels)
    
    sumCorners.append(np.sum(corners[corners != 0]))
    sumEdges.append(np.sum(edges[edges != 0]))
    sumTerraces.append(np.sum(terraces[terraces != 0]))
    sumBulk.append(np.sum(bulk[bulk != 0]))
    totalVoxels.append(np.sum(corners[corners != 0]) + np.sum(edges[edges != 0]) + np.sum(terraces[terraces != 0]) + np.sum(bulk[bulk != 0]))

    return corners, edges, terraces, bulk

def removeVoxels(corners, edges, terraces, bulk, rmCorner, rmEdge, rmTerrace, removeCorners, removeEdges, removeTerraces):

    # Rempove % of corners
    N_to_remove_corner = rmCorner
    
    if N_to_remove_corner > np.count_nonzero(corners == 1):
        print('TOO FEW CORNERS!')
        N_to_remove_corner = np.count_nonzero(corners == 1)
    
    N_removed_corner = 0

    counting_range = np.array([ [[0,0,0],[0,1,0],[0,0,0]], [[0,1,0],[1,0,1],[0,1,0]], [[0,0,0],[0,1,0],[0,0,0]] ])
    convolution = convolve(corners, counting_range, mode="constant")

    c_c = (convolution == 1); e_c = (convolution == 2); f_c = (convolution == 3)
    idx_corners_c = (c_c & corners); idx_edges_c = (e_c & corners); idx_faces_c = (f_c & corners)
    
    N_random_to_remove_corner = int(round(N_to_remove_corner - np.sum(idx_corners_c) - np.sum(idx_edges_c) - np.sum(idx_faces_c)))
    
    np.put(corners, np.random.choice(np.flatnonzero(idx_corners_c), size=np.sum(idx_corners_c), replace=False), 0)
    N_removed_corner = N_removed_corner + np.sum(idx_corners_c)
    
    np.put(corners, np.random.choice(np.flatnonzero(idx_edges_c), size=np.sum(idx_edges_c), replace=False), 0)
    N_removed_corner = N_removed_corner + np.sum(idx_edges_c)
    
    np.put(corners, np.random.choice(np.flatnonzero(idx_faces_c), size=np.sum(idx_faces_c), replace=False), 0)
    N_removed_corner = N_removed_corner + np.sum(idx_faces_c)
    
    if N_random_to_remove_corner < 0:
        N_random_to_remove_corner = 0
    else:
        np.put(corners, np.random.choice(np.flatnonzero(corners), size=N_random_to_remove_corner, replace=False), 0)
        N_removed_corner = N_removed_corner + N_random_to_remove_corner
    
    removeCorners.append(N_removed_corner)
    
    #Remove % of edges
    N_to_remove_edge = rmEdge
    
    if N_to_remove_edge > np.count_nonzero(edges == 1):
        print('Too few edges')
        N_to_remove_edge = np.count_nonzero(edges == 1)
        
    idx_edge = np.flatnonzero(edges)
    np.put(edges, np.random.choice(idx_edge, size=N_to_remove_edge, replace=False), 0)
    removeEdges.append(N_to_remove_edge)

    #Remove % of terraces
    N_to_remove_terrace = rmTerrace
    
    if N_to_remove_terrace > np.count_nonzero(terraces == 1):
        print('Too few terraces')
        N_to_remove_terrace = np.count_nonzero(terraces == 1)
        
    idx_terrace = np.flatnonzero(terraces)
    np.put(terraces, np.random.choice(idx_terrace, size=N_to_remove_terrace, replace=False), 0)
    removeTerraces.append(N_to_remove_terrace)
    
    
    # Convert to boolean
    corners_bool, edges_bool, terraces_bool, bulk_bool = convertToBoolean(corners, edges, terraces, bulk)

    return corners_bool, edges_bool, terraces_bool, bulk_bool


# ====== LOAD DATA FILE ======

# Select file
filename = '../../CALSPAR1C_init_crystal_rotated40_1650x600x1900.raw'

# Size of system
width = 1650; height = 600; depth = 1900; 
gridSize = max(width, height, depth)

# Size of grid
x,y,z = np.indices((depth, height, width))

# Read binary file
fileID = open(filename, "rb")
voxels = np.fromfile(fileID, dtype=np.uint8).reshape(depth, height, width)

fileID.close()


# ====== REMOVAL RATES ======

rmCorners  = 0.67
rmEdges    = 0.24
rmTerraces = 0.09
rmBulk     = 0.0


# ====== No. of removed voxels from experiment ======
no_rm_voxels = 130791000
iterations_per_hour = 13
total_iterations = 156

no_rm_voxels_per_iteration = no_rm_voxels/total_iterations

no_rmCorners  = int(round(rmCorners * no_rm_voxels_per_iteration))
no_rmEdges    = int(round(rmEdges * no_rm_voxels_per_iteration))
no_rmTerraces = int(round(rmTerraces * no_rm_voxels_per_iteration))


# ====== RUN SIMULATION ======

# Empty arrays
removeCorners = []; removeEdges = []; removeTerraces = []; removeBulk = []
sumCorners    = [];    sumEdges = [];    sumTerraces = [];  sumBulk   = []; totalVoxels = []

# Make folder for binary files
if not os.path.exists("binaries"):
    os.makedirs("binaries")


total_removed_voxels = 0
iteration_save_binary = [13, 39, 78, 117, 156]
    
for t in range(1, total_iterations+1):
    print("Starting iteration no. %d" %t)

    # Find number of neighbors
    print("Finding Neighbors")
    corners, edges, terraces, bulk = findNeighbors(voxels, sumCorners, sumEdges, sumTerraces, sumBulk, totalVoxels)

    # Remove voxels (corners, edges, terraces)
    print("Remove voxels")
    corners_bool, edges_bool, terraces_bool, bulk_bool = removeVoxels(corners, edges, terraces, bulk, no_rmCorners, no_rmEdges, no_rmTerraces, removeCorners, removeEdges,
                                                                      removeTerraces)
    # Put together to one array (voxels)
    voxels = np.asarray(corners_bool | edges_bool | terraces_bool | bulk_bool, dtype=np.int8)

    total_removed_voxels = total_removed_voxels + removeCorners[-1] + removeEdges[-1] + removeTerraces[-1]

    print(total_removed_voxels)

    # Save output data
    np.savetxt('removedCorners.txt', removeCorners); np.savetxt('removedEdges.txt', removeEdges); np.savetxt('removedTerraces.txt', removeTerraces)
    np.savetxt('sumCorners.txt', sumCorners); np.savetxt('sumEdges.txt', sumEdges); np.savetxt('sumTerraces.txt', sumTerraces)
    np.savetxt('totalRemovedVoxels.txt', totalVoxels)
    
    if t == iteration_save_binary[0]:
        print('Save binary file')
        output = open("binaries/output%03d.raw" % t, "wb")
        output.write(voxels)
        output.close()
        
        iteration_save_binary = iteration_save_binary[1:]
