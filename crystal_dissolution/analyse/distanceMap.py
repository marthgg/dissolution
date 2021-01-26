import numpy as np
from scipy.ndimage import binary_erosion
from scipy import ndimage

def createFileForDistanceMap(fileID_initial, fileID_step, width, depth, height, outputFileName):
    # Save data files in array and reshape to correct size
    data_initial  = np.fromfile(fileID_initial,  dtype=np.uint8).reshape(depth, height, width)
    data_step  = np.fromfile(fileID_step,  dtype=np.uint8).reshape(depth, height, width)

    # Calculate amount of erosion
    calculate_erosion_step  = binary_erosion(data_step)

    # Find difference between binary image and amount of erosion
    erosion_step  = data_step-calculate_erosion_step

    # Calculate distance map at t0
    distmap_initial = ndimage.distance_transform_edt(data_initial)

    # Find retreat around the crystal during deltaT=ti-t0
    retreat = distmap_initial*erosion_step

    # Save data as a txt file that can be loaded to make the plot
    # Write the array to disk
    with open(outputfilename, 'w') as outfile:
        outfile.write('# Array shape: {0}\n'.format(retreat.shape))
        
        for data_slice in retreat:
            np.savetxt(outfile, data_slice, fmt='%-7.2f')
            outfile.write('# New slice\n')