import numpy as np
import matplotlib.pyplot as plt

# No. of removed voxels
removedCorners = np.loadtxt('removedCorners.txt')
removedEdges = np.loadtxt('removedEdges.txt')
removedTerraces = np.loadtxt('removedTerraces.txt')

# No. of voxels left in simulations
sumCorners = np.loadtxt('sumCorners.txt')
sumEdges = np.loadtxt('sumEdges.txt')
sumTerraces = np.loadtxt('sumTerraces.txt')

# Cumulative numbers
cum_corners = np.cumsum(removedCorners)
cum_edges = np.cumsum(removedEdges)
cum_terraces = np.cumsum(removedTerraces)

totalRemovedVoxels = cum_corners + cum_edges + cum_terraces

# Dissolved voxels divided by surface area
dissolvedVoxels = removedCorners + removedEdges + removedTerraces
surfaceArea = 3*sumCorners + 2*sumEdges + sumTerraces

# Make figures
plt.figure(1)
plt.title('Cumulative plot of removed voxels')
plt.plot(cum_corners, 'DeepSkyBlue', lineWidth=2, label='Corners')
plt.plot(cum_edges, 'RoyalBlue',  lineWidth=2, label='Edges')
plt.plot(cum_terraces, 'DarkBlue', linewidth=2, label='Terraces')
plt.plot(totalRemovedVoxels, 'black',  lineWidth=2, label='Total')
plt.xlabel('Iterations')
plt.ylabel('No. of removed voxels')
plt.legend()

plt.figure(2)
plt.title('No. of dissolved voxels per surface area')
plt.plot(dissolvedVoxels/surfaceArea,  'black', lineWidth=2, label='Total')
plt.plot(removedCorners/surfaceArea, 'DeepSkyBlue',  lineWidth=2, label='Corners')
plt.plot(removedEdges/surfaceArea, 'RoyalBlue',  lineWidth=2, label='Edges')
plt.plot(removedTerraces/surfaceArea, 'DarkBlue', lineWidth=2, label='Terraces')
plt.xlabel('Iterations')
plt.ylabel('Dissolved voxels/surface area')
plt.legend()

plt.show()