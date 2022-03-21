from random import random as rand

""" 二维蓝噪声采样 """

class BNS:

    def __init__(self, points, R=2e-4):
        # points [{'id','lat','lng','kde'}]
        self.points = []
        self.point_index = {}
        self.disks = []
        self.rate = 100
        for p in points:
            self.point_index[p['id']] = len(self.points)
            p['r'] = float(R) / p['kde']
            self.points.append(p)
        self.indexes = {
            "ready": [p["id"] for p in self.points],
            "active": [],
            "seed": [],
            "disactivated": []
        }

    def apply_sample(self):
        # 迭代
        while len(self.indexes["active"]) + len(self.indexes["ready"]) > 0:
            print(len(self.indexes["active"]) + len(self.indexes["ready"]))
            # 取一个种子点
            seed = self._get_random_point()
            if seed != -1:
                self._create_disk(seed)
        all_count = len(self.points)
        sample_count = len(self.indexes['seed'])
        # print(f"all {all_count} sampling {sample_count} rate {sample_count / all_count}")
        self.rate = round(sample_count / all_count, 2)
        return self.disks

    def _get_random_point(self):
        if len(self.indexes["active"]) == 0:
            # 从所有就绪点中随机选一个作为种子点
            seed = self.indexes["ready"].pop(int(rand() * len(self.indexes["ready"])))
            self.indexes["seed"].append(seed)
            return seed

        # 从所有活跃点中随机选一个作为种子点
        seed = self.indexes["active"].pop(int(rand() * len(self.indexes["active"])))
        self.indexes["seed"].append(seed)
        return seed

    def _create_disk(self, pid):
        seed = self.points[self.point_index[pid]]
        r = seed["r"]

        next_ready = []
        next_active = []

        children = [pid]

        # 扫描剩余活跃点
        for i in self.indexes["active"]:
            target = self.points[self.point_index[i]]

            dist = ((target["lat"] - seed["lat"]) ** 2 + (target["lng"] - seed["lng"]) ** 2) ** 0.5

            if dist < r:
                # (0, r] -> 加入失效点
                self.indexes["disactivated"].append(i)
                children.append(i)
            else:
                next_active.append(i)

        # 扫描剩余就绪点
        for i in self.indexes["ready"]:
            target = self.points[self.point_index[i]]

            dist = ((target["lat"] - seed["lat"]) ** 2 + (target["lng"] - seed["lng"]) ** 2) ** 0.5

            if dist > 2 * r:
                # 放回
                next_ready.append(i)
            elif dist > r:
                # (1r, 2r] -> 加入活跃点
                next_active.append(i)
            else:
                # (0, r] -> 加入失效点
                self.indexes["disactivated"].append(i)
                children.append(i)
        sample_point = self.point_index[pid]
        sample_point['children'] = children
        self.disks.append(sample_point)

        self.indexes["ready"] = [i for i in next_ready]
        self.indexes["active"] = [i for i in next_active]

        return