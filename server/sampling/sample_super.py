import json
import random


def load_kde_data(filename_origin):
    with open("../data/kde_" + filename_origin + ".json", mode='r') as fin:
        kde_data = json.load(fin)
        matrix = kde_data["matrix"]
    return matrix


def load_origin_data(filename_origin, n_cluster):
    with open("../data/" + filename_origin + "$class=" + str(n_cluster) + ".json", 'r') as fr:
        population = json.load(fr)
    return population


def apply_super_bns(population, method, rate, c):
    populationDic = {i['id']: [i['id'], i['lat'], i['lng'], i['value'], i['vLabel']] for i in population}
    with open(f'../data/{method}_{filename_origin}$rate={rate}$count={c}.json', 'r') as fr:
        disks = json.load(fr)

    data_processed = []

    for disk in disks:
        value = 0
        labels = {}
        max_count = 0
        max_label = -1
        for index in disk["children"]:
            value += populationDic[index][3]
            labels[populationDic[index][4]] = labels.get(populationDic[index][4], [])
            labels[populationDic[index][4]].append(index)

        for key in labels:
            if len(labels[key]) > max_count:
                max_count = len(labels[key])
                max_label = key
        lat = 0
        lng = 0
        distance = []
        if max_label != -1:
            percent = len(labels[max_label]) / len(disk["children"])
            if 1 / 2 <= percent <= 2 / 3:
                for i in labels[max_label]:
                    lat += populationDic[i][1]
                    lng += populationDic[i][2]
                lat /= len(labels[max_label])
                lng /= len(labels[max_label])
                for i in labels[max_label]:
                    distance.append({'id': i, 'distance': ((lat - populationDic[i][1]) ** 2
                                                           + (lng - populationDic[i][2]) ** 2) ** 0.5})
                distance.sort(key=lambda x: x['distance'])
                p = populationDic[distance[0]['id']]
            else:
                p = populationDic[disk["id"]]
        else:
            p = populationDic[disk["id"]]
        center = populationDic[disk["id"]]

        point = {
            "id": p[0],
            "lat": p[1],
            "lng": p[2],
            "value": p[3],
            # 以下是新的字段
            "diskId": disk["diskId"],
            "children": disk["children"],
            "radius": disk["radius"],
            "averVal": value / len(disk["children"]),
            "center": center[0]
        }

        data_processed.append(point)

    with open(f"../data/super_{method}_{filename_origin}$class={n_cluster}$rate={str(rate)}$count={str(c)}.json", 'w') as f:
        json.dump(data_processed, f)


def apply_super_super_bns(population, method, rate, c):
    populationDic = {i['id']: [i['id'], i['lat'], i['lng'], i['value'], i['vLabel']] for i in population}
    with open(f'../data/{method}_{filename_origin}$rate={rate}$count={c}.json', 'r') as fr:
        disks = json.load(fr)

    data_processed = []

    for disk in disks:
        value = 0
        labels = {}
        labels_percent = []
        for index in disk["children"]:
            value += populationDic[index][3]
            labels[populationDic[index][4]] = labels.get(populationDic[index][4], [])
            labels[populationDic[index][4]].append(index)

        for key in labels:
            labels_percent.append({'label': key, 'children': labels[key], 'percent': len(labels[key]) / len(disk["children"])})
        labels_percent.sort(key=lambda x: x['percent'], reverse=True)
        labels_percent_top = labels_percent[:5]
        flag = True
        for top_label in labels_percent_top:
            if 1 / 4 <= top_label['percent'] <= 2 / 3:
                flag = False
                lat = 0
                lng = 0
                distance = []
                for k in top_label['children']:
                    lat += populationDic[k][1]
                    lng += populationDic[k][2]
                lat /= len(top_label['children'])
                lng /= len(top_label['children'])
                for k in top_label['children']:
                    distance.append({'id': k, 'distance': ((lat - populationDic[k][1]) ** 2
                                                           + (lng - populationDic[k][2]) ** 2) ** 0.5})
                distance.sort(key=lambda x: x['distance'])
                p = populationDic[distance[0]['id']]

                point = {
                    "id": p[0],
                    "lat": p[1],
                    "lng": p[2],
                    "value": p[3],
                    # 以下是新的字段
                    # "diskId": disk["diskId"],
                    # "children": disk["children"],
                    # "radius": disk["radius"],
                    # "averVal": value / len(disk["children"]),
                    # "center": center[0]
                }

                data_processed.append(point)
        if flag:
            p = populationDic[disk["id"]]
            point = {
                "id": p[0],
                "lat": p[1],
                "lng": p[2],
                "value": p[3],
                # 以下是新的字段
                # "diskId": disk["diskId"],
                # "children": disk["children"],
                # "radius": disk["radius"],
                # "averVal": value / len(disk["children"]),
                # "center": center[0]
            }

            data_processed.append(point)

    print(len(disks) / len(population))
    print(len(data_processed) / len(population))

    with open(f"../data/super_{method}_{filename_origin}$class={n_cluster}$rate={str(rate)}$count={str(c)}.json", 'w') as f:
        json.dump(data_processed, f)


if __name__ == "__main__":

    filename_origin = 'Poverty'
    rate_arr = [0.01, 0.05, 0.1]
    count = 1
    n_cluster = 8

    population = load_origin_data(filename_origin, n_cluster)
    for rate in rate_arr:
        for i in range(count):
            apply_super_super_bns(population, 'bns', rate, i)
