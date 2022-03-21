import copy

import networkx as nx
import numpy as np
from scipy.spatial import Delaunay
import math
import time

""" 构建三角剖分网 """
def create_delaunay(points):
    """
    :param points: [[lat,lng]...]
    :param indexs: 点的索引
    :return:networkx.Graph
    """
    print("开始构建三角网")
    tri = Delaunay(np.array(points))
    g = nx.Graph()
    edges = []
    distance_dic = {i: {} for i in range(len(points))}
    for simplice in tri.simplices:
        for edge in [[0, 1], [0, 2], [1, 2]]:
            source = simplice[edge[0]]
            target = simplice[edge[1]]
            weight = math.sqrt(math.pow(points[source][0]-points[target][0], 2)+math.pow(points[source][1]-points[target][1], 2))
            edges.append([source, target, weight])
            distance_dic[source][target] = weight
            distance_dic[target][source] = weight
    g.add_weighted_edges_from(edges)
    std_array = []
    mean_dic = {}
    remove_edges = []
    for node in g.nodes():
        neighbors = list(nx.neighbors(g, node))
        neighbors.append(node)
        distance = []
        for i in neighbors:
            for j in distance_dic[i]:
                if j in neighbors:
                    distance.append(distance_dic[i][j])
        distance = np.array(distance)
        mean = np.mean(distance)
        mean_dic[node] = mean
        std = np.std(distance)
        std_array.append(std)
    global_std = np.mean(np.array(std_array))
    for node in g.nodes():
        neighbors = nx.neighbors(g, node)
        for i in neighbors:
            distance = distance_dic[node][i]
            if distance > mean_dic[node] + global_std:
                remove_edges.append([node, i])
    g.remove_edges_from(remove_edges)
    print(f'共{len(edges)}条边，删除{len(remove_edges)}条边')
    return g


""" 计算邻域属性熵 """
def attribute_entropy(values):
    """
    :param values: 邻域属性值 [float...]
    :return: float
    """
    value_sum = np.sum(values)
    p = [i / value_sum for i in values]
    H = 0
    for i in p:
        H += -i*math.log2(i)
    H /= len(p)
    return H


""" 计算信息熵相似性 """
def info_entropy_similarity(value, values):
    similarity = attribute_entropy(np.append(values, value))

    return similarity


""" 递归搜索邻居 """
def find_neighbors(node, neighbors_dic, values ,seta, labels_indes):
    neighbors = neighbors_dic[node]['neighbors']
    labels_index_undirect = []
    labels_indes_copy = copy.deepcopy(labels_indes)
    for i in range(len(neighbors) - 1):
        if neighbors_dic[neighbors[i]]['flag'] is False:
            if info_entropy_similarity(values[neighbors[i]], values[labels_indes_copy.extend(labels_index_undirect)]) > seta:
                labels_index_undirect.append(neighbors[i])
                neighbors_dic[neighbors[i]]['flag'] = True
    # for i in range(len(labels_index_undirect)):
    #     labels_index_undirect.extend(find_neighbors(labels_index_undirect[i], neighbors_dic, values, seta))
    return labels_index_undirect


""" 基于属性熵的空间聚类具体过程 """
def clustering_process(graph, values, seta):
    entropy_array = []
    neighbors_dic = {}
    nodes = graph.nodes()
    for node in nodes:
        neighbors = list(nx.neighbors(graph, node))
        neighbors.append(node)
        value_neighbors = values[neighbors]
        entropy = attribute_entropy(value_neighbors)
        entropy_array.append({'node': node, 'neighbors': neighbors, 'entropy': entropy})
        neighbors_dic[node] = {'neighbors': neighbors, 'flag': False}
    entropy_array.sort(key=lambda x: x['entropy'], reverse=True)

    labels_index = []
    select_center = entropy_array[0]
    neighbors = select_center['neighbors']
    labels_index.append(select_center['node'])
    for i in range(len(neighbors)-1):
        if neighbors_dic[neighbors[i]]['flag'] is False:
            if info_entropy_similarity(values[neighbors[i]], values[labels_index]) > seta or len(labels_index) < 4:
                labels_index.append(neighbors[i])
                neighbors_dic[neighbors[i]]['flag'] = True
    labels_index_undirected = []
    for i in range(len(labels_index)-1):
        labels_index_undirected.extend(find_neighbors(labels_index[i], neighbors_dic, values, seta, labels_index))
    labels_index.extend(labels_index_undirected)
    while len(labels_index_undirected) > 0:
        labels_index_undirected_copy = copy.deepcopy(labels_index_undirected)
        labels_index_undirected = []
        for i in range(len(labels_index_undirected_copy) - 1):
            labels_index_undirected.extend(find_neighbors(labels_index_undirected_copy[i], neighbors_dic, values, seta, labels_index))
        labels_index.extend(labels_index_undirected)
    return labels_index


def clustering(graph, values, seta):
    labels_index_all = []
    left_nodes_count = len(graph.nodes())
    while left_nodes_count > 0:
        print(f'第{len(labels_index_all)}类，还剩{left_nodes_count}个点')
        one_class_index = clustering_process(graph, values, seta)
        graph.remove_nodes_from(one_class_index)
        labels_index_all.append(one_class_index)
        left_nodes_count -= len(one_class_index)
    print('还剩0个点')
    return labels_index_all


def add_labels(data, labels):
    for i in range(len(labels)):
        for j in labels[i]:
            data[j]['vLabel'] = i
    return data

def all_process(data, seta):
    points = []
    values = []
    for i in range(len(data)):
        points.append([data[i]['lat'], data[i]['lng']])
        if data[i]['value'] == 0:
            values.append(1)
        else:
            values.append(data[i]['value']*100)
    values = np.array(values)
    g = create_delaunay(points)

    labels_index = clustering(g, values, seta)
    return add_labels(data, labels_index), len(labels_index)


if __name__ == "__main__":
    import json

    start = time.time()
    seta = 0.2
    fileName = "Occupation"
    with open(f'../data/{fileName}.json', 'r') as fr:
        data = json.load(fr)
    data, n_cluster = all_process(data, seta)
    with open(f'../data/{fileName}$class={n_cluster}.json', 'w') as fw:
        json.dump(data, fw)
    end = time.time()
    print(str(end - start))
