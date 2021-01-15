import numpy as np
from mayavi import mlab

from analyse.makeFigure import plotFigure

# ====== LOAD DATA FILE ======

# Select file
filename = 'binaries/output001.raw'

# Size of system
width = 165; height = 60; depth = 190; 

# Read binary file
fileID = open(filename, "rb")
voxels = np.fromfile(fileID, dtype=np.uint8).reshape(depth, height, width)

fileID.close()

# ====== MAKE FIGURE ======

# Colors for 3: Corners, 4:Edges, 5:Terraces
color_types = {3:(0,0.1,1), 4:(0,.6, 1), 5:(1, 0,1), 6:(0,1,0)}

plotFigure(voxels, color_types)

mlab.show()
