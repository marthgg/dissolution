import numpy as np
import copy
import random

def makeClusters(percentImpurity, voxels, height, depth, width, minCluster, maxCluster):
    impurities = copy.deepcopy(voxels)
    impurities.fill(0)

    idx_voxels = np.flatnonzero(voxels)
    n_impurityVoxels = int(round(percentImpurity*np.count_nonzero(voxels == 1)))

    clusterOptions = ["alt1", "alt2", "alt3", "alt4", "alt5", "alt6"]

    for m in range(0, n_impurityVoxels):

        randomPosition = np.random.choice(idx_voxels)
        np.put(impurities, randomPosition, 1)
        
        clusterSize = random.randint(minCluster,maxCluster)
        selectedOption = random.sample(clusterOptions, clusterSize-1)

        for selectOption in selectedOption:
            if selectOption == "alt1":
                alt1 = randomPosition + height
                np.put(impurities, alt1, 1)
            
            if selectOption == "alt2":
                alt2 = randomPosition - height
                np.put(impurities, alt2, 1)

            if selectOption == "alt3":
                alt3 = randomPosition + 1
                np.put(impurities, alt3, 1)
            
            if selectOption == "alt4":
                alt4 = randomPosition - 1
                np.put(impurities, alt4, 1)

            if selectOption == "alt5":
                alt5 = randomPosition + (width*width)
                np.put(impurities, alt5, 1)
            
            if selectOption == "alt6":
                alt6 = randomPosition - (width*width)
                np.put(impurities, alt6, 1)

        sumImpurities = np.sum(impurities[impurities != 0])
        
        if sumImpurities > n_impurityVoxels:
            break

    return impurities


def createDislocation(voxels, dislocationHeight, dislocationDepth, depth):
    dislocations = copy.deepcopy(voxels)
    dislocations.fill(0)

    idx_voxels = np.flatnonzero(voxels)

    if dislocationHeight != 0 and dislocationDepth != 0:
        randomPosition = np.random.choice(idx_voxels)
        np.put(dislocations, randomPosition, 1)

        for i in range(dislocationHeight):
            np.put(dislocations, randomPosition+i, 1)
            for j in range(dislocationDepth):
                np.put(dislocations, randomPosition+i+(depth*depth*j), 1)

    return dislocations