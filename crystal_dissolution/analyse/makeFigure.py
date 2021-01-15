import numpy as np
from mayavi import mlab

# Find neighbors for plotting
def findNeighbors(voxels):
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
    #print("Convolution\n", type(voxels), np.sum(convolution))
    corners = (convolution == 3) | (convolution == 2) | (convolution == 1)
    edges = (convolution == 4)
    terraces = (convolution == 5)
    bulk = (convolution == 6)
    
    corners = (corners & voxels)
    edges = (edges & voxels)
    terraces = (terraces & voxels)
    bulk = (bulk & voxels)

    corners_bool = np.array(corners, dtype=bool)
    edges_bool = np.array(edges, dtype=bool)
    terraces_bool = np.array(terraces, dtype=bool)
    bulk_bool = np.array(bulk, dtype=bool)

    site_types = np.zeros(voxels.shape, dtype=np.float64)
    site_types[corners==1] = 3
    site_types[edges==1] = 4
    site_types[terraces==1] = 5
    site_types[bulk==1] = 6

    return corners_bool, edges_bool, terraces_bool, bulk_bool, site_types


def plotFigure(voxels, color_types):
    corners_bool, edges_bool, terraces_bool, bulk_bool, site_types= findNeighbors(voxels)
    site_types = np.asarray(site_types, dtype=np.float64)
    voxels = np.asarray(corners_bool | edges_bool | terraces_bool | bulk_bool, dtype=np.float64)

    for i, color in color_types.items():
        xx, yy, zz = np.where(site_types == i)
        mlab.points3d(xx, yy, zz,mode="cube", color=color,scale_factor=1)