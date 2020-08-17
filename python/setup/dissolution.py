import numpy as np

def findNeighbors(voxels, impurities, corners, edges, terraces, bulk, dislocations, sumCorners, sumEdges, sumTerraces, sumImpurities, sumBulk, totalVoxels):
    for i in range(1, voxels.shape[0]-1):
        for j in range(1, voxels.shape[1]-1):
            for k in range(1, voxels.shape[2]-1):
                n = 0
                if voxels[i,j,k] == 1:
                    if voxels[i+1, j, k] == 1:
                        n += 1
                    if voxels[i-1, j, k] == 1:
                        n += 1
                    if voxels[i, j+1, k] == 1:
                        n += 1
                    if voxels[i, j-1, k] == 1:
                        n += 1
                    if voxels[i, j, k+1] == 1:
                        n += 1
                    if voxels[i, j, k-1] == 1:
                        n += 1
                    
                    if dislocations[i+1, j, k] == 1:
                        n -= 1
                    if dislocations[i-1, j, k] == 1:
                        n -= 1
                    if dislocations[i, j+1, k] == 1:
                        n -= 1
                    if dislocations[i, j-1, k] == 1:
                        n -= 1
                    if dislocations[i, j, k+1] == 1:
                        n -= 1
                    if dislocations[i, j, k-1] == 1:
                        n -= 1

                if n == 3 or n == 2 or n == 1:
                    if impurities[i,j,k] == 0:
                        corners[i,j,k] = 1
                if n == 4:
                    if impurities[i,j,k] == 0:
                        edges[i,j,k] = 1
                if n == 5:
                    if impurities[i,j,k] == 0:
                        terraces[i,j,k] = 1
                if n == 6:
                    if impurities[i,j,k] == 0:
                        bulk[i,j,k] = 1


                if impurities[i,j,k] == 1:
                    m = 0
                    if voxels[i+1, j, k] == 1: 
                        m += 1
                    if voxels[i-1, j, k] == 1: 
                        m += 1
                    if voxels[i, j+1, k] == 1:
                        m += 1
                    if voxels[i, j-1, k] == 1:
                        m += 1
                    if voxels[i, j, k+1] == 1:
                        m += 1
                    if voxels[i, j, k-1] == 1:
                        m += 1


                    #Remove impurities if it is floating free
                    if m == 0: 
                        impurities[i,j,k] = 0
                                        
                    if m == 1 and (impurities[i+1, j, k] == 1 or impurities[i-1, j, k] == 1 or impurities[i, j+1, k] == 1 or impurities[i, j-1, k] == 1 or impurities[i, j, k+1] == 1 or impurities[i, j, k-1] == 1):
                        impurities[i,j,k] = 0

                    if m == 2 and ((impurities[i+1, j, k] == 1 and impurities[i-1, j, k] == 1) or \
                            (impurities[i+1, j, k] == 1 and impurities[i, j+1, k] == 1) or \
                            (impurities[i+1, j, k] == 1 and impurities[i, j-1, k] == 1) or \
                            (impurities[i+1, j, k] == 1 and impurities[i, j, k+1] == 1) or \
                            (impurities[i+1, j, k] == 1 and impurities[i, j, k-1] == 1) or \
                            (impurities[i-1, j, k] == 1 and impurities[i, j+1, k] == 1) or \
                            (impurities[i-1, j, k] == 1 and impurities[i, j-1, k] == 1) or \
                            (impurities[i-1, j, k] == 1 and impurities[i, j, k+1] == 1) or \
                            (impurities[i-1, j, k] == 1 and impurities[i, j, k-1] == 1) or \
                            (impurities[i, j+1, k] == 1 and impurities[i, j-1, k] == 1) or \
                            (impurities[i, j+1, k] == 1 and impurities[i, j, k+1] == 1) or \
                            (impurities[i, j+1, k] == 1 and impurities[i, j, k-1] == 1) or \
                            (impurities[i, j-1, k] == 1 and impurities[i, j, k+1] == 1) or \
                            (impurities[i, j-1, k] == 1 and impurities[i, j, k-1] == 1) or \
                            (impurities[i, j, k+1] == 1 and impurities[i, j, k-1] == 1)):
                        impurities[i,j,k] = 0

    
    sumCorners.append(np.sum(corners[corners != 0]))
    sumEdges.append(np.sum(edges[edges != 0]))
    sumTerraces.append(np.sum(terraces[terraces != 0]))
    sumImpurities.append(np.sum(impurities[impurities != 0]))
    sumBulk.append(np.sum(bulk[bulk != 0]))
    totalVoxels.append(np.sum(corners[corners != 0]) + np.sum(edges[edges != 0]) + np.sum(terraces[terraces != 0]) + np.sum(impurities[impurities != 0]) + np.sum(bulk[bulk != 0]))

    return corners, edges, terraces, bulk, impurities, dislocations



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
    

    return corners, edges, terraces, bulk