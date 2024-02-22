import numpy as np
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath("C:/Users/Miriam_Esteve/OneDrive - Fundación Universitaria San Pablo CEU/Documents/CEU/Investigación/2023/UTHECA/paper/scripts/Python/"))
import pers_diagram
import classification
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# parameters
ar = 0.001
sd0 = 1

# Read data
datas = []
for i in range(1, 100):
    datas.append(pd.read_csv("C:/Users/Miriam_Esteve/OneDrive - Fundación Universitaria San Pablo CEU/Documents/CEU/Investigación/2023/UTHECA/paper/scripts/data/len100/data" + str(i) + "_ar" + str(ar) + "-sd0" + str(sd0)+ ".csv")[["x", "y"]])


# Rips diagram
rips = pers_diagram.Rips(maxdim=1, coeff=2)
diagrams = [rips.fit_transform(data) for data in datas]
diagrams_h1 = [rips.fit_transform(data)[1] for data in datas]


# Compute homology of each dataset
plt.figure(figsize=(12,6))
plt.suptitle('Compute homology of each dataset. ar = ' + str(ar) + ", sd0 = " + str(sd0))

for i in range(8):
    ax = plt.subplot(240+i+1)
    rips.plot(diagrams[i], show=False)
    plt.title("PD of $H_1$ for data" + str(i))
plt.show()

# Persistence diagram
pimgr = pers_diagram.PersistenceImager(pixel_size=0.1)
pimgr.fit(diagrams_h1)
imgs = pimgr.transform(diagrams_h1)

#Plot diagram
plt.figure(figsize=(15,7.5))
plt.suptitle('Compute persistence diagram. ar = ' + str(ar) + ", sd0 = " + str(sd0))

for i in range(8):
    ax = plt.subplot(240+i+1)
    pimgr.plot_diagram(diagrams_h1[i], ax)
    plt.title("PI of $H_1$ for data" + str(i))

plt.show()

# Plot persistence image
plt.figure(figsize=(15,7.5))
plt.suptitle('Compute persistence images. ar = ' + str(ar) + ", sd0 = " + str(sd0))

for i in range(8):
    ax = plt.subplot(240+i+1)
    pimgr.plot_image(imgs[i], ax)
    plt.title("PI of $H_1$ for data" + str(i))

# Classify the datasets from the persistence images
imgs_array = [img.flatten() for img in imgs]
classification.classification_persim(imgs_array)
