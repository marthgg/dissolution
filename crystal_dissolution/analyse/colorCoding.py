import numpy as np

# Color scale to use when plotting with ax.voxels
def setColorsMatplotlib(voxels, corners_bool, edges_bool, terraces_bool, bulk_bool):
    colors = np.empty(voxels.shape, dtype=object)
    colors[corners_bool]      = 'DeepSkyBlue'
    colors[edges_bool]        = 'RoyalBlue'
    colors[terraces_bool]     = 'DarkBlue'
    colors[bulk_bool]         = 'DarkGrey'

    return colors