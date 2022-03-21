import json
from sampling.bns import BNS


def apply_bns(filename_origin, R):

    with open("./data/kde_" + filename_origin + ".json", mode='r') as fin:
        kde_data = json.load(fin)
        population = kde_data["population"]
        matrix = kde_data["matrix"]

    populationDic = {i[0]: i for i in population}

    bns = BNS(matrix, R=R)

    seeds, disks = bns.apply_sample()

    data_processed = []

    for disk in disks:
        value = 0
        for index in disk["children"]:
            value += populationDic[index][3]

        p = populationDic[disk["seedId"]]

        point = {
            "id": p[0],
            "lat": p[1],
            "lng": p[2],
            "value": p[3],
            # 以下是新的字段
            "diskId": disk["id"],
            "children": disk["children"],
            "radius": disk["r"],
            "averVal": value / len(disk["children"])
        }

        data_processed.append(point)

    with open("./data/bns_" + filename_origin + "$rate=" + str(bns.rate) + ".json", mode='w') as f:
        json.dump(data_processed, f)
    return data_processed, bns


if __name__ == "__main__":
    filename_origin = 'Poverty'
    R = 0.034
    count = 1
    with open("../data/kde_" + filename_origin + ".json", mode='r') as fin:
        kde_data = json.load(fin)
        population = kde_data["population"]
        matrix = kde_data["matrix"]
    populationDic = {i[0]: i for i in population}

    for i in range(count):
        bns = BNS(matrix, R=R)

        seeds, disks = bns.apply_sample()
        print(len(seeds), len(disks))
        data_processed = []

        for disk in disks:
            value = 0
            for index in disk["children"]:
                value += populationDic[index][3]

            p = populationDic[disk["seedId"]]

            point = {
                "id": p[0],
                "lat": p[1],
                "lng": p[2],
                "value": p[3],
                # 以下是新的字段
                "diskId": disk["id"],
                "children": disk["children"],
                "radius": disk["r"],
                "averVal": value / len(disk["children"])
            }

            data_processed.append(point)

        with open("../data/bns_" + filename_origin + "$rate=" + str(bns.rate) + "$count=" + str(i) + ".json", mode='w') as f:
            json.dump(data_processed, f)
        if bns.rate in [0.01, 0.05, 0.1]:
            with open("./rate_bns.json", 'r') as fr:
                rate_json = json.load(fr)
            if filename_origin in rate_json:
                rate_json[filename_origin][str(bns.rate)] = R
            else:
                rate_json[filename_origin] = {}
                rate_json[filename_origin][str(bns.rate)] = R
            with open("./rate_bns.json", 'w') as fw:
                json.dump(rate_json, fw)

    print(0)    # 程序运行完成

    pass
