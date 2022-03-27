from random import random as rand

DEBUG = False

""" 二维蓝噪声采样 """
class BNS:

    def __init__(self, points, R=2e-4):
        # points: np.array shape=(5, N) --5: id, screenX, screenY, value, kde
        self.points = []
        self.point_index = {}
        self.disks = []
        self.rate = 100
        for p in points:
            self.point_index[p[0]] = len(self.points)
            self.points.append({
                "id": int(p[0]),
                "x": p[1],
                "y": p[2],
                "val": p[3],
                "r": float(R) / p[4]
            })
        self.indexes = {
            "ready": [p["id"] for p in self.points],
            "active": [],
            "seed": [],
            "disactivated": []
        }

    def apply_sample(self):
        # 迭代
        while len(self.indexes["active"]) + len(self.indexes["ready"]) > 0:
            if DEBUG:
                print(len(self.indexes["active"]) + len(self.indexes["ready"]))
            # 取一个种子点
            seed = self._get_random_point()
            if seed != -1:
                self._create_disk(seed)
        all_count = len(self.points)
        sample_count = len(self.indexes['seed'])
        if DEBUG:
            print(f"all {all_count} sampling {sample_count} rate {sample_count/all_count}")
        self.rate = round(sample_count/all_count, 2)
        return self.indexes["seed"], self.disks

    # def _get_random_point(self):
    #     flag = False
    #     seed = -1
    #     if len(self.indexes["active"]) == 0:
    #         # 从所有就绪点中随机选一个作为种子点
    #         while len(self.indexes["ready"]) > 0 and flag is False:
    #             seed = self.indexes["ready"].pop(int(rand() * len(self.indexes["ready"])))
    #             flag = self._judge_random_point(seed)
    #             if flag is False:
    #                 seed = -1
    #                 self.indexes["disactivated"].append(seed)
    #             else:
    #                 self.indexes["seed"].append(seed)
    #                 return seed
    #
    #     # 从所有活跃点中随机选一个作为种子点
    #     while len(self.indexes["active"]) > 0 and flag is False:
    #         seed = self.indexes["active"].pop(int(rand() * len(self.indexes["active"])))
    #         flag = self._judge_random_point(seed)
    #         if flag is False:
    #             seed = -1
    #             self.indexes["disactivated"].append(seed)
    #         else:
    #             self.indexes["seed"].append(seed)
    #             return seed
    #     return seed
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

    def _judge_random_point(self, index):
        seed = self.points[self.point_index[index]]
        r = seed["r"]
        flag = True
        for disk in self.disks:
            tr = disk["r"]
            dist = (
                    (disk["x"] - seed["x"]) ** 2 + (disk["y"] - seed["y"]) ** 2
                   ) ** 0.5
            max_r = max(r, tr)
            if max_r > dist:
                flag = False
        return flag

    def _create_disk(self, index):
        seed = self.points[self.point_index[index]]
        r = seed["r"]

        next_ready = []
        next_active = []

        children = [index]
        for disk in self.disks:
            dist = (
                (disk["x"] - seed["x"]) ** 2 + (disk["y"] - seed["y"]) ** 2
            ) ** 0.5
            r = min(r, dist)

        
        # 扫描剩余活跃点
        for i in self.indexes["active"]:
            target = self.points[self.point_index[i]]

            dist = (
                (target["x"] - seed["x"]) ** 2
                + (target["y"] - seed["y"]) ** 2
            ) ** 0.5

            if dist < r:
                # (0, r] -> 加入失效点
                self.indexes["disactivated"].append(i)
                children.append(i)
            else:
                next_active.append(i)
        
        # 扫描剩余就绪点
        for i in self.indexes["ready"]:
            target = self.points[self.point_index[i]]

            dist = (
                (target["x"] - seed["x"]) ** 2
                + (target["y"] - seed["y"]) ** 2
            ) ** 0.5

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
