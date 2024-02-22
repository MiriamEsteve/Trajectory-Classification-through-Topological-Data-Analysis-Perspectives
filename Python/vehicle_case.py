import numpy as np
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath("C:/Users/Miriam_Esteve/OneDrive - Fundación Universitaria San Pablo CEU/Documents/CEU/Investigación/2023/UTHECA/paper/scripts/Python/"))
import pers_diagram
#import barycenter
import gudhi
print("Current gudhi version:", gudhi.__version__)
print("Version >= 3.2.0 is required for this tutorial")
from gudhi.wasserstein.barycenter import lagrangian_barycenter as bary
from gudhi.persistence_graphical_tools import plot_persistence_diagram

import Wasserstein_distance
import classification
import matplotlib.pyplot as plt
plt.style.use('ggplot')


# Read data
data = pd.read_csv("C:/Users/Miriam_Esteve/OneDrive - Fundación Universitaria San Pablo CEU/Documents/CEU/Investigación/2023/UTHECA/paper/dataset/data.csv")

# Unique vehicle
unique_value = np.unique(data["Vehicle_ID"])

datas = []
for i in range(len(unique_value)):
    datas.append(data[data["Vehicle_ID"] == unique_value[i]][["Local_X", "Local_Y"]])


datas = []
for i in range(10,18):
    datas.append(data[data["Vehicle_ID"] == unique_value[i]][["Local_X", "Local_Y"]])

# Rips diagram
rips = pers_diagram.Rips(maxdim=1, coeff=2)
diagrams = [rips.fit_transform(data) for data in datas]
diagrams_h1 = [rips.fit_transform(data)[1] for data in datas]

# Drop specific row
index = []
for i in range(len(diagrams_h1)):
    if len(diagrams_h1[i]) > 10:
        print(i)
        index.append(i)

diagrams_h1 = [diagrams_h1[i] for i in index]

# Compute homology of each dataset
plt.figure(figsize=(12,6))
plt.suptitle('Compute homology of each dataset.')

for i in range(8):
    ax = plt.subplot(240+i+1)
    rips.plot(diagrams[i], show=False)
    plt.title("PD of $H_1$ for Ship_" + str(i))
plt.show()

# Persistence diagram
pimgr = pers_diagram.PersistenceImager(pixel_size=0.1)
pimgr.fit(diagrams_h1)
imgs = pimgr.transform(diagrams_h1)

#Plot diagram
plt.figure(figsize=(15,7.5))
plt.suptitle('Compute persistence diagram')

for i in range(8):
    ax = plt.subplot(240+i+1)
    pimgr.plot_diagram(diagrams_h1[i], ax)
    plt.title("PI of $H_1$ for Ship_" + str(i))

plt.show()

# Plot persistence image
plt.figure(figsize=(15,7.5))
plt.suptitle('Compute persistence images')

for i in range(8):
    ax = plt.subplot(240+i+1)
    pimgr.plot_image(imgs[i], ax)
    plt.title("PI of $H_1$ for Ship_" + str(i))

# Classify the datasets from the persistence images
imgs_array = [img.flatten() for img in imgs]
classification.classification_persim(imgs_array)

# Barycenter of three vehicles
datas = []
datas.append(data[data["Vehicle_ID"] == unique_value[1]][["Local_X", "Local_Y"]])
datas.append(data[data["Vehicle_ID"] == unique_value[2]][["Local_X", "Local_Y"]])
datas.append(data[data["Vehicle_ID"] == unique_value[3]][["Local_X", "Local_Y"]])

# Rips diagram of three vehicles
rips = pers_diagram.Rips(maxdim=1, coeff=2)
diagrams = [rips.fit_transform(data) for data in datas]
diagrams_h1 = [rips.fit_transform(data)[1] for data in datas]

diags = diagrams_h1.copy()

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
colors=[ "red", "blue", "green" ]
for diag, c in zip(diags, colors):
    plot_persistence_diagram(diag, axes=ax, colormap=c)
ax.set_title("Set of 2 persistence diagrams", fontsize=22)

def proj_on_diag(x):
    return ((x[1] + x[0]) / 2, (x[1] + x[0]) / 2)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)

for diag, c in zip(diags, colors):
    plot_persistence_diagram(diag, axes=ax, colormap=c)

def plot_bary(b, diags, groupings, axes):
    # n_y = len(Y.points)
    for i in range(len(diags)):
        indices = G[i]
        n_i = len(diags[i])

        for (y_j, x_i_j) in indices:
            y = b[y_j]
            if y[0] != y[1]:
                if x_i_j >= 0:  # not mapped with the diag
                    x = diags[i][x_i_j]
                else:  # y_j is matched to the diagonal
                    x = proj_on_diag(y)
                ax.plot([y[0], x[0]], [y[1], x[1]], c='black',
                        linestyle="dashed")

    ax.scatter(b[:,0], b[:,1], color='purple', marker='d', label="barycenter (estim)")
    ax.legend()
    ax.set_title("Set of diagrams and their barycenter", fontsize=22)

b, log = bary(diags,
         init=0,
         verbose=True)  # we initialize our estimation on the first diagram (the red one.)
G = log["groupings"]
plot_bary(b, diags, G, axes=ax)