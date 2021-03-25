import numpy as np
import matplotlib.pyplot as plt

# Files containing the retreat
retreat_files = ['retreat/retreat_026.txt', 'retreat/retreat_036.txt', 'retreat/retreat_045.txt']

# Size of each voxel
pixel_size = 0.325 # micrometer

# Time (hour):
time = [6, 9, 12]

# Labels
labels = ['t3-init', 't4-init', 't5-init']

counter = 0

for retreat_file in retreat_files:
    fileID = np.loadtxt(retreat_file)

    # Dissolution rate
    dissolution_rate = (fileID * pixel_size) / time[counter]
    dissolution_rate = dissolution_rate[dissolution_rate != 0]

    # Create histograms
    elements = np.linspace(0, 5, 50, endpoint=True)

    hist, bins = np.histogram(dissolution_rate, bins=elements)
    frequency = hist/len(dissolution_rate)

    # Plot figure
    plt.figure(1)
    plt.plot(bins[1:], frequency, label=labels[counter], linewidth=3)

    plt.xlabel('Dissolution rate (µm/h)')
    plt.ylabel('Frequency')
    
    counter += 1



#plt.xlim([0.5, 2.5])
plt.legend()

plt.show()