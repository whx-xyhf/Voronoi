from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from jenkspy import JenksNaturalBreaks
import pandas as pd
import json

n_cluster = 8
eps = 0.06
filename_origin = 'Occupation'
with open(f'../data/{filename_origin}.json', 'r') as fr:
    data = json.load(fr)
value = []
points = []
for i in data:
    value.append(i['value'])
    points.append([i['lat'], i['lng']])

print("start JenksNaturalBreaks")
# 属性聚类
jnb = JenksNaturalBreaks(nb_class=n_cluster)
jnb.fit(value)
labels = jnb.labels_

print("DBSCAN")
# 空间聚类
points = StandardScaler().fit_transform(points)
db = DBSCAN(eps=eps, min_samples=1).fit(points)
labels_db = db.labels_
print(f"空间{len(set(labels_db))}类")

for i in range(len(data)):
    data[i]['label1'] = int(labels[i])
    data[i]['label2'] = int(labels_db[i])

print("common...")
df = pd.DataFrame(data, index=range(len(data)))
group = df.groupby(['label1', 'label2'])
final_label_dic = {}
class_index = 0
for i in group:
    indexes = group.get_group(i[:][0]).index.tolist()
    for j in indexes:
        final_label_dic[j] = class_index
    class_index += 1

for i in range(len(data)):
    data[i]['label'] = int(final_label_dic[i])

print(f'最终聚类{class_index}')
with open(f'../data/{filename_origin}$class={class_index}.json', 'w') as fw:
    json.dump(data, fw)
