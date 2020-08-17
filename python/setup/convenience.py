import numpy as np
import matplotlib.pyplot as plt
import glob
from PIL import Image

def convertToBoolean(corners, edges, terraces, bulk, impurities, dislocations):
    corners_bool = np.array(corners, dtype=bool)
    edges_bool = np.array(edges, dtype=bool)
    terraces_bool = np.array(terraces, dtype=bool)
    bulk_bool = np.array(bulk, dtype=bool)
    impurities_bool = np.array(impurities, dtype=bool)
    dislocations_bool = np.array(dislocations, dtype=bool)
    
    return corners_bool, edges_bool, terraces_bool, bulk_bool, impurities_bool, dislocations_bool
    

def setColors(voxels, corners_bool, edges_bool, terraces_bool, bulk_bool, impurities_bool, dislocations_bool):
    colors = np.empty(voxels.shape, dtype=object)
    colors[corners_bool]      = 'DeepSkyBlue'
    colors[edges_bool]        = 'RoyalBlue'
    colors[terraces_bool]     = 'DarkBlue'
    colors[bulk_bool]         = 'DarkGrey'
    colors[impurities_bool]   = 'Purple'
    colors[dislocations_bool] = 'Green'

    return colors


def emptyMatrixes(x,y,z):
    corners      = np.zeros((x.shape[0], y.shape[1], z.shape[2]))
    edges        = np.zeros((x.shape[0], y.shape[1], z.shape[2]))
    terraces     = np.zeros((x.shape[0], y.shape[1], z.shape[2]))
    bulk         = np.zeros((x.shape[0], y.shape[1], z.shape[2]))

    return corners, edges, terraces, bulk


def plotFigure(voxels, size, colors):
    fig = plt.figure(figsize=(15,12))
    ax = fig.gca(projection='3d')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    ax.voxels(voxels, facecolors=colors, edgecolor='k', lineWidth=0.1, shade=False)

    ax.set_xlim(0,size)
    ax.set_ylim(0,size)
    ax.set_zlim(0,size)


def makeGIF():
    print("making GIF")

    fp_in = "images/plot*.png"
    fp_out = "dissolution.gif"

    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=200, loop=0)