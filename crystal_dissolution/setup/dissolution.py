import numpy as np

def convertToBoolean(corners, edges, terraces, bulk):
    corners_bool = np.array(corners, dtype=bool)
    edges_bool = np.array(edges, dtype=bool)
    terraces_bool = np.array(terraces, dtype=bool)
    bulk_bool = np.array(bulk, dtype=bool)
    
    return corners_bool, edges_bool, terraces_bool, bulk_bool


def findNeighbors(voxels, sumCorners, sumEdges, sumTerraces, sumBulk, totalVoxels):
    counting_range = np.array([ [[0,0,0], 
                             [0,1,0], 
                             [0,0,0]], 
                            [[0,1,0], 
                             [1,0,1], 
                             [0,1,0]],
                            [[0,0,0], 
                             [0,1,0], 
                             [0,0,0]] ])

    from scipy.ndimage import convolve
    convolution = convolve(voxels, counting_range, mode="constant")
    #print("Convolution\n", type(voxels), convolution)
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


def removeVoxels(corners, edges, terraces, bulk, rmCorner, rmEdge, rmTerrace, rmBulk, removeCorners, removeEdges, removeTerraces, removeBulk):

    # Rempove % of corners
    idx_corner = np.flatnonzero(corners)
    N_to_remove_corner = int(round(rmCorner*np.count_nonzero(corners == 1)))
    np.put(corners, np.random.choice(idx_corner, size=N_to_remove_corner, replace=False), 0)
    removeCorners.append(N_to_remove_corner)

    #Remove % of edges
    idx_edge = np.flatnonzero(edges)
    N_to_remove_edge = int(round(rmEdge*np.count_nonzero(edges == 1)))
    np.put(edges, np.random.choice(idx_edge, size=N_to_remove_edge, replace=False), 0)
    removeEdges.append(N_to_remove_edge)

    #Remove % of terraces
    idx_terrace = np.flatnonzero(terraces)
    N_to_remove_terrace = int(round(rmTerrace*np.count_nonzero(terraces == 1)))
    np.put(terraces, np.random.choice(idx_terrace, size=N_to_remove_terrace, replace=False), 0)
    removeTerraces.append(N_to_remove_terrace)

    #Remove % of bulk
    idx_bulk = np.flatnonzero(bulk)
    N_to_remove_bulk = int(round(rmBulk*np.count_nonzero(bulk == 1)))
    np.put(bulk, np.random.choice(idx_bulk, size=N_to_remove_bulk, replace=False), 0)
    removeBulk.append(N_to_remove_bulk)
    
    corners_bool, edges_bool, terraces_bool, bulk_bool = convertToBoolean(corners, edges, terraces, bulk)

    return corners_bool, edges_bool, terraces_bool, bulk_bool