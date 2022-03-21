from random import random as rand
import math
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

""" 分组蓝噪声采样 """


class ZDHXBNS:

    def __init__(self, points, R=2e-4, min_r_rate=1.1):
        # points: np.array shape=(5, N) --5: id, screenX, screenY, value, kde
        self.points = []
        self.point_index = {}
        self.disks = []
        self.min_r_rate = min_r_rate
        self.rate = 100
        for p in points:
            self.point_index[p[0]] = len(self.points)
            self.points.append({
                "id": int(p[0]),
                "x": p[1],
                "y": p[2],
                "val": p[3],
                "ss": p[5],

                "r": float(R) / p[4],
                "lat": p[1],
                "lng": p[2]
            })
        min_r = min(self.points, key=lambda x: x['r'])['r']
        self.min_r = min_r * self.min_r_rate
        # self.adjust_radius()
        self.indexes = {
            "ready": [p for p in self.points],
            "active": [],
            "seed": [],
            "disactivated": []
        }

    def adjust_radius(self):
        # 计算信息熵
        X = [[i['x'], i['y']] for i in self.points]
        distance_metrics = euclidean_distances(X)
        for i in range(len(self.points)):
            index_neighbor = np.where(distance_metrics[i] <= self.points[i]['r'])[0]
            labels = [self.points[j]['ss'] for j in index_neighbor]
            entropy = self._attribute_entropy(labels)
            self.points[i]['entropy'] = entropy

    def _attribute_entropy(self, labels):
        count = len(labels)
        lebels_set = list(set(labels))
        p = [labels.count(i) / count for i in lebels_set]
        H = 0
        for i in p:
            H += -i * math.log2(i)
        return H

    def apply_sample(self):
        # 迭代
        while len(self.indexes["active"]) + len(self.indexes["ready"]) > 0:
            print(len(self.indexes["active"]) + len(self.indexes["ready"]))
            # 取一个种子点
            seed = self._get_random_point()
            self._create_disk(seed)
        all_count = len(self.points)
        sample_count = len(self.indexes['seed'])
        print(f"all {all_count} sampling {sample_count} rate {sample_count / all_count}")
        self.rate = round(sample_count / all_count, 2)
        return self.indexes["seed"], self.disks

    # def _get_random_point(self):
    #     if len(self.indexes["active"]) == 0:
    #         # 从所有就绪点中随机选一个作为种子点
    #         seed_point = max(self.indexes["ready"], key=lambda x: x['entropy'])
    #         seed = seed_point['id']
    #         self.indexes["ready"].remove(seed_point)
    #         self.indexes["seed"].append(seed)
    #         return seed
    #     # 从所有活跃点中随机选一个作为种子点
    #     seed_point = max(self.indexes["active"], key=lambda x: x['entropy'])
    #     seed = seed_point['id']
    #     self.indexes["active"].remove(seed_point)
    #     self.indexes["seed"].append(seed)
    #
    #     return seed

    def _get_random_point(self):
        if len(self.indexes["active"]) == 0:
            # 从所有就绪点中随机选一个作为种子点
            seed = self.indexes["ready"].pop(int(rand() * len(self.indexes["ready"])))['id']
            self.indexes["seed"].append(seed)
            return seed

        # 从所有活跃点中随机选一个作为种子点
        seed = self.indexes["active"].pop(int(rand() * len(self.indexes["active"])))['id']
        self.indexes["seed"].append(seed)
        return seed

    def _create_disk(self, index):
        seed = self.points[self.point_index[index]]
        r = seed["r"]

        # for disk in self.disks:
        #     dist = (
        #                    (disk["x"] - seed["x"]) ** 2 + (disk["y"] - seed["y"]) ** 2
        #            ) ** 0.5
        #     r = min(r, dist)
        #     if r < self.min_r:
        #         r = self.min_r
        #         break

        r = max(r, self.min_r)
        # 查找邻近包含点
        # if r > self.min_r:
        array = []
        for p in self.points:
            dist = ((p["x"] - seed["x"]) ** 2 + (p["y"] - seed["y"]) ** 2) ** 0.5
            if dist <= r:
                array.append(p)
        labels = [p['ss'] for p in array]
        entropy = self._attribute_entropy(labels)
        # 调整半径
        # r = max(r / (1 + entropy/len(labels)), self.min_r)
        r = (r - self.min_r) / (1 + entropy) + self.min_r
        # r = r - (r - self.min_r) / (1 + entropy)
        # r = max(r, self.min_r)

        next_ready = []
        next_active = []

        children = [index]

        # 扫描剩余活跃点
        for i in self.indexes["active"]:

            dist = (
                           (i["x"] - seed["x"]) ** 2 + (i["y"] - seed["y"]) ** 2
                   ) ** 0.5

            if dist < r:
                # (0, r] -> 加入失效点
                self.indexes["disactivated"].append(i['id'])
                children.append(i['id'])
            else:
                next_active.append(i)

        # 扫描剩余就绪点
        for i in self.indexes["ready"]:
            dist = (
                           (i["x"] - seed["x"]) ** 2 + (i["y"] - seed["y"]) ** 2
                   ) ** 0.5

            if dist > 2 * r:
                # 放回
                next_ready.append(i)
            elif dist > r:
                # (1r, 2r] -> 加入活跃点
                next_active.append(i)
            else:
                # (0, r] -> 加入失效点
                self.indexes["disactivated"].append(i['id'])
                children.append(i['id'])

        self.disks.append({
            "id": len(self.indexes["seed"]) - 1,
            "seedId": index,
            "children": children,
            "x": seed["x"],
            "y": seed["y"],
            "r": r
        })

        self.indexes["ready"] = [i for i in next_ready]
        self.indexes["active"] = [i for i in next_active]

        return
