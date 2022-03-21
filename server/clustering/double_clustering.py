from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from jenkspy import JenksNaturalBreaks
import json
n_cluster = 12
eps = 0.1
filename_origin = 'Occupation'
with open(f'../data/{filename_origin}.json', 'r') as fr:
    data = json.load(fr)

# 先做属性聚类
value = [i['value'] for i in data]
jnb = JenksNaturalBreaks(nb_class=n_cluster)
jnb.fit(value)
labels = jnb.labels_

labels_data = [[] for i in range(n_cluster)]

for i in range(len(labels)):
    data[i]['vLabel'] = int(labels[i])
    labels_data[labels[i]].append(data[i])
double_labels_data = []

# 对每一类做dbscan
print("start dbscan")
for i in range(len(labels_data)):
    points = StandardScaler().fit_transform([[j['lat'], j['lng']] for j in labels_data[i]])
    db = DBSCAN(eps=eps, min_samples=1).fit(points)
    labels_db = db.labels_
    count = len(set(labels_db))
    second_labels = [[] for j in range(count)]
    for j in range(len(labels_db)):
        second_labels[labels_db[j]].append(labels_data[i][j])
    double_labels_data.extend(second_labels)

double_labels_data_dic = {}
for i in range(len(double_labels_data)):
    for j in double_labels_data[i]:
        double_labels_data_dic[j['id']] = i

for i in range(len(data)):
    data[i]['label'] = double_labels_data_dic[data[i]['id']]

print(len(double_labels_data))
with open(f'../data/{filename_origin}$class={n_cluster}.json', 'w') as fw:
    json.dump(data, fw)



# # 取类中心点
# sample_points = []
# for i in range(len(double_labels_data)):
#     print(i)
#     lat = 0
#     lng = 0
#     for j in range(len(double_labels_data[i])):
#         lat += double_labels_data[i][j]['lat']
#         lng += double_labels_data[i][j]['lng']
#     lat /= len(double_labels_data[i])
#     lng /= len(double_labels_data[i])
#     for j in range(len(double_labels_data[i])):
#         dis = ((double_labels_data[i][j]['lat'] - lat) ** 2 + (double_labels_data[i][j]['lng'] - lng) ** 2) ** 0.5
#         double_labels_data[i][j]['distance'] = dis
#     sample_points.append(min(double_labels_data[i], key=lambda x: x['distance']))
#
# rate = round(len(double_labels_data)/len(data), 2)
# print('sampling count', len(double_labels_data))
# print('sampling rate', rate)
# if rate in [0.01, 0.05, 0.1]:
#     with open("../data/double_" + filename_origin + "$class=" + str(n_cluster) + "$rate=" + str(rate) + "$count=" + str(0) + ".json", mode='w') as f:
#         json.dump(sample_points, f)
