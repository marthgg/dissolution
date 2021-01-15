import numpy as np

def convertToBoolean(corners, edges, terraces, bulk):
    corners_bool = np.array(corners, dtype=bool)
    edges_bool = np.array(edges, dtype=bool)
    terraces_bool = np.array(terraces, dtype=bool)
    bulk_bool = np.array(bulk, dtype=bool)
    
    return corners_bool, edges_bool, terraces_bool, bulk_bool