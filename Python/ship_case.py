import transbigdata as tbd
import geopandas as gpd
from gridify.gridify import gridify
import pygradus
import shapely.geometry
import pandas as pd
import numpy as np
import importlib

path = "C:/Users/Miriam_Esteve/OneDrive - Fundación Universitaria San Pablo CEU/Documents/CEU/Investigación/2023/UTHECA/paper/datasetShip/datasets/"

grid = gridify.area_to_grid(side_length=10000)

ais = pd.read_csv(path + "training_set.csv", parse_dates = ['timestamp'])
ais.head()

ais_subset = ais[['timestamp', 'mmsi', 'lat', 'lon', 'speed', 'course', 'vessel_type']]

%time ais_subset.head(10).speed.iloc[::-1].rolling(3).sum().iloc[::-1]
%time ais_subset['grid_point'] = ais_subset.apply(lambda row: grid.get_grid_point(row.lat, row.lon), axis=1)
%time ais_subset['node'] = ais_subset.apply(lambda row: grid.get_grid_position(row), axis=1)

ports = pd.read_csv(path + 'ports.csv')
ports = ports[['port_id', 'lat', 'lon']]
ports.head()

ais_ports = pd.read_csv(path + 'ports_calculated_from_ais.csv')
ais_ports = ais_ports[['id', 'lat', 'lon']]
ais_ports.head()

%time ais_ports['grid_point'] = ais_ports.apply(lambda row: grid.get_grid_point(row.lat, row.lon), axis=1)
%time ais_ports['node'] = ais_ports.apply(lambda row: grid.get_grid_position(row), axis=1)

ports_subset = ports[['port_id', 'node']]
ports_subset[ports_subset.port_id == 941].head()


test = ais_subset[(ais_subset.mmsi == 276807000) | (ais_subset.mmsi == 265004000)]
test = ais_subset[ais_subset.mmsi == 205453000]
#test = ais_subset[ais_subset.lat > 58].head(100000)
test = ais_subset.head(500000)
# plot all AIS
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap  # import Basemap matplotlib toolkit


test = test.reset_index(drop=True)
test = test.sort_values(by=['mmsi', 'timestamp'])

observations_by_vessels = test.groupby('mmsi')

graph = []

fig = plt.figure(figsize=(30,30))

m = Basemap(llcrnrlon = ais.lon.min(),llcrnrlat = ais.lat.min(), urcrnrlon = ais.lon.max(),
           urcrnrlat = ais.lat.max(),
           resolution='h')
m.shadedrelief()
for mmsi, observations in observations_by_vessels:
    xy = observations.loc[:, ('lat', 'lon')]
    plt.plot(xy.loc[:, ('lon')], xy.loc[:, ('lat')], 'o', c=np.random.rand(3,), alpha=1, markersize=1)
plt.show()