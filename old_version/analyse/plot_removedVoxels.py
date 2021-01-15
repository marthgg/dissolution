import numpy as np
import matplotlib.pyplot as plt

# Corners: 100 %, Edges: 50 %, Terraces: 0 %, Impurity: 0 %
removedCorners_100_50_0_0 = np.loadtxt('corners100_edges50_terraces0_impurity0/removedCorners.txt')
removedEdges_100_50_0_0 = np.loadtxt('corners100_edges50_terraces0_impurity0/removedEdges.txt')
sumCorners_100_50_0_0 = np.loadtxt('corners100_edges50_terraces0_impurity0/sumCorners.txt')
sumEdges_100_50_0_0 = np.loadtxt('corners100_edges50_terraces0_impurity0/sumEdges.txt')
sumTerraces_100_50_0_0 = np.loadtxt('corners100_edges50_terraces0_impurity0/sumTerraces.txt')

# Cumulative numbers
cum_corners_100_50_0_0 = np.cumsum(removedCorners_100_50_0_0)
cum_edges_100_50_0_0 = np.cumsum(removedEdges_100_50_0_0)

totalRemovedVoxels_100_50_0_0 = cum_corners_100_50_0_0 + cum_edges_100_50_0_0

# Dissolved voxels divided by surface area
dissolvedVoxels_100_50_0_0 = removedCorners_100_50_0_0 + removedEdges_100_50_0_0
surfaceArea_100_50_0_0 = 3*sumCorners_100_50_0_0[1:] + 2*sumEdges_100_50_0_0[1:] + sumTerraces_100_50_0_0[1:]


# Corners: 100 %, Edges: 50 %, Terraces: 0 %, Impurity: 5 %
removedCorners_100_50_0_5 = np.loadtxt('corners100_edges50_terraces0_impurity5/removedCorners.txt')
removedEdges_100_50_0_5 = np.loadtxt('corners100_edges50_terraces0_impurity5/removedEdges.txt')
sumCorners_100_50_0_5 = np.loadtxt('corners100_edges50_terraces0_impurity5/sumCorners.txt')
sumEdges_100_50_0_5 = np.loadtxt('corners100_edges50_terraces0_impurity5/sumEdges.txt')
sumTerraces_100_50_0_5 = np.loadtxt('corners100_edges50_terraces0_impurity5/sumTerraces.txt')

# Cumulative numbers
cum_corners_100_50_0_5 = np.cumsum(removedCorners_100_50_0_5)
cum_edges_100_50_0_5 = np.cumsum(removedEdges_100_50_0_5)

totalRemovedVoxels_100_50_0_5 = cum_corners_100_50_0_5 + cum_edges_100_50_0_5

# Dissolved voxels divided by surface area
dissolvedVoxels_100_50_0_5 = removedCorners_100_50_0_5 + removedEdges_100_50_0_5
surfaceArea_100_50_0_5 = 3*sumCorners_100_50_0_5[1:] + 2*sumEdges_100_50_0_5[1:] + sumTerraces_100_50_0_5[1:]


plt.figure(1)
plt.subplot(221)
plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.2, hspace=0.3)
plt.plot(cum_corners_100_50_0_0, 'DeepSkyBlue', lineWidth=2, label='Corners')
plt.plot(cum_edges_100_50_0_0, 'RoyalBlue',  lineWidth=2, label='Edges')
plt.plot(totalRemovedVoxels_100_50_0_0, 'black',  lineWidth=2, label='Total')
plt.title('Corners: 100 %, Edges: 50 %, Terraces: 0 %, Impurity elements: 0 %')
plt.xlabel('Iterations')
plt.ylabel('No. of removed voxels')
plt.ylim([0,1000000])
plt.legend()

plt.subplot(222)
plt.plot(cum_corners_100_50_0_5, 'DeepSkyBlue', lineWidth=2, label='Corners')
plt.plot(cum_edges_100_50_0_5, 'RoyalBlue',  lineWidth=2, label='Edges')
plt.plot(totalRemovedVoxels_100_50_0_5, 'black',  lineWidth=2, label='Total')
plt.title('Corners: 100 %, Edges: 50 %, Terraces: 0 %, Impurity elements: 5 %')
plt.xlabel('Iterations')
plt.ylabel('No. of removed voxels')
plt.ylim([0,1000000])
plt.legend()

plt.subplot(223)
plt.title('Corners: 100 %, Edges: 50 %, Terraces: 0 %, Impurity elements: 0 %')
plt.plot(dissolvedVoxels_100_50_0_0/surfaceArea_100_50_0_0, 'black', lineWidth=2, label='Total')
plt.plot(removedCorners_100_50_0_0/surfaceArea_100_50_0_0, 'DeepSkyBlue',  lineWidth=2, label='Corners')
plt.plot(removedEdges_100_50_0_0/surfaceArea_100_50_0_0, 'RoyalBlue',  lineWidth=2, label='Edges')
plt.xlabel('Iterations')
plt.ylabel('Dissolved voxels/surface area')
plt.legend()

plt.subplot(224)
plt.title('Corners: 100 %, Edges: 50 %, Terraces: 0 %, Impurity elements: 5 %')
plt.plot(dissolvedVoxels_100_50_0_5/surfaceArea_100_50_0_5, 'black', lineWidth=2, label='Total')
plt.plot(removedCorners_100_50_0_5/surfaceArea_100_50_0_5, 'DeepSkyBlue',  lineWidth=2, label='Corners')
plt.plot(removedEdges_100_50_0_5/surfaceArea_100_50_0_5, 'RoyalBlue',  lineWidth=2, label='Edges')
plt.xlabel('Iterations')
plt.ylabel('Dissolved voxels/surface area')
plt.legend()

plt.show()