import json
from sampling.zdhxbns import ZDHXBNS
import time


def translate(array, target_left, target_right):
    source_left = min(array)
    source_right = max(array)
    source_step = source_right - source_left
    target_step = target_right - target_left
    return [(i - source_left)/source_step*target_step+target_left for i in array]


if __name__ == "__main__":
    start = time.time()
    filename_origin = 'Occupation'
    R = 0.081
    count = 1
    n_cluster = 8
    min_R_rate = 1
    with open("../data/kde_" + filename_origin + ".json", mode='r') as fin:
        kde_data = json.load(fin)
        population = kde_data["population"]
        matrix = kde_data["matrix"]
    with open("../data/" + filename_origin + "$class=" + str(n_cluster) + ".json", 'r') as fr:
        origin_data = json.load(fr)
    origin_data_dic = {i['id']: i for i in origin_data}
    # lat = []
    # lng = []
    for i in range(len(matrix)):
        matrix[i].append(origin_data_dic[int(matrix[i][0])]['label'])
    #     lat.append(matrix[i][1])
    #     lng.append(matrix[i][2])
    # new_lat = translate(lat, 0, 300)
    # new_lng = translate(lng, 0, 200)
    # for i in range(len(matrix)):
    #     matrix[i].append(new_lat[i])
    #     matrix[i].append(new_lng[i])
    populationDic = {i[0]: i for i in population}

    for i in range(count):
        sssssbns = ZDHXBNS(matrix, R=R, min_r_rate=min_R_rate)

        seeds, disks = sssssbns.apply_sample()
        print(len(seeds), len(disks))
        data_processed = []

        for disk in disks:
            p = populationDic[disk["seedId"]]
            point = {
                "id": p[0],
                "lat": p[1],
                "lng": p[2],
                "value": p[3],
                "label": origin_data_dic[p[0]]['label'],
                # 以下是新的字段
                "diskId": disk["id"],
                "children": disk["children"],
                "radius": disk["r"],
            }

            data_processed.append(point)

        if sssssbns.rate in [0.01, 0.05, 0.1]:
            with open("../data/zdhxbns1_" + filename_origin + "$class=" + str(n_cluster) + "$rate=" + str(
                    sssssbns.rate) + "$min_r=" + str(min_R_rate) + "$count=" + str(i) + ".json", mode='w') as f:
                json.dump(data_processed, f)
            with open("./rate_zdhxbns1.json", 'r') as fr:
                rate_json = json.load(fr)
            if filename_origin in rate_json:
                if str(n_cluster) in rate_json[filename_origin]:
                    rate_json[filename_origin][str(n_cluster)][str(sssssbns.rate)] = R
                else:
                    rate_json[filename_origin][str(n_cluster)] = {str(sssssbns.rate): R}
            else:
                rate_json[filename_origin] = {str(n_cluster): {}}
                rate_json[filename_origin][str(n_cluster)][str(sssssbns.rate)] = R
            with open("./rate_zdhxbns1.json", 'w') as fw:
                json.dump(rate_json, fw)
    end = time.time()
    print(end - start)
