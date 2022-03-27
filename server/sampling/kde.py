import sys
import numpy as np
import time
import json
from scipy import stats


""" 生成核密度矩阵 （耗时长） """
def build_matrix(population):
    a1 = []
    a2 = []
    a3 = []
    for p in population:
        a1.append(p[1])
        a2.append(p[2])
        a3.append(p[3])
    m1 = np.asarray(a1)
    m2 = np.asarray(a2)
    m3 = np.asarray(a3)
    xmin = m1.min()
    xmax = m1.max()
    ymin = m2.min()
    ymax = m2.max()
    X, Y = np.mgrid[xmin : xmax : 2, ymin : ymax : 2]

    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([m1, m2])
    try:
        kernel = stats.gaussian_kde(values)
    except:
        print(values)
    Z = np.reshape(kernel(positions).T, X.shape)


    kde = [kernel([p[1], p[2]])[0] for p in population]
    m4 = np.asarray(kde)
    indexes = [p[0] for p in population]
    mid = np.asarray(indexes)

    matrix = np.vstack([mid, m1, m2, m3, m4])
    return matrix.T


def normalizated_array(array):
    m3 = [d[2] for d in array]
    vmin = min(m3)
    vmax = max(m3)
    vp = vmax - vmin
    return [[d[0], d[1], (d[2] - vmin) / vp] for d in array]

def get_population(data):
    return [[d['id'], d['lat'], d['lng'], d['value']] for d in data]

def get_kde(data_snapshot):

    values = [[d['id'], d['lat'], d['lng'], d['value']] for d in data_snapshot]
    matrix = build_matrix(values)

    return matrix, values

if __name__ == "__main__":

    with open("./server/dataSet/Density.json", 'r+') as f:
        tmp = json.load(f)
    matrix, population = get_kde(tmp)
    print(matrix)
    print(matrix.shape)

    # filename_origin = 'Density.json'
    # with open("../data/" + filename_origin, mode='r') as f:
    #     data_snapshot = json.load(f)

    # # [id, x, y, val]][]
    # values = [[d['id'], d['lat'], d['lng'], d['value']] for d in data_snapshot]
    # matrix = build_matrix(values)

    # with open("../data/kde_" + filename_origin, mode='w') as fout:
    #     json.dump({
    #         "population": values,
    #         "matrix": matrix.tolist()
    #     }, fout)

    # print(0)    # 程序运行完成

    # pass

