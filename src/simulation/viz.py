from matplotlib import pyplot as plt
import numpy as np

with open('output', 'r') as in_file:
    data = in_file.readlines()
    for i in range(len(data)):
        if i % 5 == 0:
            items = data[i].split()
            intensity = []
            for item in items:
                intensity.append(float(item.strip('[,]')))
            intensity = np.array(intensity)
            intensity = intensity.reshape((2, 3))
            print(intensity)
            print(intensity.shape)

            plt.imshow(intensity, cmap='gist_heat', interpolation='nearest', vmin=0, vmax=1)
            plt.colorbar()
            plt.savefig(filename=str(int(i / 5)).zfill(2) + '.svg')
            plt.clf()
