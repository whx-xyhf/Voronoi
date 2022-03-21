import numpy as np
import libpysal
import geopandas as gpd
from spopt.region.skater import Skater
from sklearn.metrics import pairwise as skm

chicago = gpd.read_file('../data/Chicago77.shp')

w = libpysal.weights.Queen.from_dataframe(chicago)
for i in chicago:
    print(i)
# print(chicago)
# attrs_name = ['num_spots']
# n_clusters = 10
# floor = 3
# trace = False
# islands = "increase"
# spanning_forest_kwds = dict(dissimilarity=skm.manhattan_distances, affinity=None, reduction=np.sum, center=np.mean)
#
# model = Skater(chicago, w, attrs_name, n_clusters, floor, trace, islands, spanning_forest_kwds)
# model.solve()
#
#
# model.labels_
#
# chicago['skater_new'] = model.labels_
# chicago.plot(column='skater_new', categorical=True, figsize=(12, 8), edgecolor='w')
