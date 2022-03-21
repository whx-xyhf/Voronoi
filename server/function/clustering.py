from jenkspy import JenksNaturalBreaks
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


class Clustering:
    def __init__(self, data):
        self.data = data
        pass

    def n_break(self, n_cluster, eps):
        # 先做属性聚类
        value = [i['value'] for i in self.data]
        jnb = JenksNaturalBreaks(nb_class=n_cluster)
        jnb.fit(value)
        labels = jnb.labels_

        labels_data = [[] for i in range(n_cluster)]

        for i in range(len(labels)):
            self.data[i]['vLabel'] = int(labels[i])
            labels_data[labels[i]].append(self.data[i])

        # 再对每一类做dbscan
        self.dbscan(eps, labels_data)

    def mean_break(self, n_cluster, eps):
        # 先做区间划分
        value = [i['value'] for i in self.data]
        v_min = min(value)
        v_max = max(value)
        step = (v_max - v_min) / n_cluster
        labels_data = [[] for i in range(n_cluster)]
        for i in range(len(value)):
            label = int((value[i] - v_min) / step) - 1
            if label == -1:
                label = 0
            self.data[i]['vLabel'] = label
            labels_data[label].append(self.data[i])
        # 再对每一类做dbscan
        self.dbscan(eps, labels_data)
        return self.data

    def dbscan(self, eps, labels_data):
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

        for i in range(len(self.data)):
            self.data[i]['label'] = double_labels_data_dic[self.data[i]['id']]
        return self.data
