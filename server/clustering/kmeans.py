import numpy as np
from sklearn.cluster import KMeans
from jenkspy import JenksNaturalBreaks
import json
n_cluster = 8
fileName = 'Density'
with open(f'../data/{fileName}.json', 'r') as fr:
    data = json.load(fr)
value = [i['value'] for i in data]
# km = KMeans(n_clusters=n_cluster).fit(np.array(value).reshape(-1, 1))
# labels = km.labels_
jnb = JenksNaturalBreaks(nb_class=n_cluster)
jnb.fit(value)
labels = jnb.labels_
for i in range(len(data)):
    data[i]['vLabel'] = int(labels[i])
print(jnb.breaks_)
with open(f'../data/{fileName}$class={n_cluster}.json', 'w') as fw:
    json.dump(data, fw)
