import networkx as nx
import numpy as np
from scipy.spatial import Delaunay
import math
import time
from sklearn.cluster import KMeans

""" 构建三角剖分网 """
def create_delaunay(points, indexs):
    """
    :param points: [[lat,lng]...]
    :param indexs: 点的索引
    :return:networkx.Graph
    """
    print("开始构建三角网")
    tri = Delaunay(np.array(points))
    g = nx.Graph()
    edges = []
    for simplice in tri.simplices:
        for edge in [[0, 1], [0, 2], [1, 2]]:
            source = simplice[edge[0]]
            target = simplice[edge[1]]
            weight = math.pow(points[source][0]-points[target][0], 2)+math.pow(points[source][1]-points[target][1], 2)
            edges.append([indexs[source], indexs[target], weight])
    g.add_weighted_edges_from(edges)
    return g


""" 初始化最小生成树 """
def init_min_spaning_tree(graph):
    """
    :param graph: networkx.graph  三角网
    :return: [[source,target],...]
    """
    print("初始化最小生成树")
    edges = list(nx.minimum_spanning_edges(graph,data=False))
    g = nx.Graph()
    g.add_edges_from(edges)
    return edges, g.nodes()


""" 切割树生成子树直到树的数量满足聚类个数 """
def cut_tree(trees, values, n_cluster):
    """
    :param trees: [{edges:初始的最小生成树的边,std:float,node:[]},...] 初始树没有std 和 node
    :param values: 点对应的属性值 np.array
    :param n_cluster: 最终的聚类个数
    :return:
    """
    current_count=len(trees)
    print(f'正在分类 已有{current_count}类')
    if len(trees) < n_cluster:
        #选择属性标准差最大的树切割
        select_tree_edges = trees.pop(0)['edges']
        g = nx.Graph()
        g.add_edges_from(select_tree_edges)
        cut_edges = []
        index=0
        for edge in select_tree_edges:
            index+=1
            print(f'第{current_count}类，第{index}个边')
            degree_source = nx.degree(g, edge[0])
            #选择包含度不为1的点的边切割
            if degree_source > 1:
                degree_target = nx.degree(g, edge[1])
                if degree_target > 1:
                    #切割
                    g.remove_edge(edge[0], edge[1])
                    sub_graphs = nx.connected_component_subgraphs(g)
                    std = max([np.std(values[sub.nodes()]) for sub in sub_graphs])
                    cut_edges.append({'edge': edge, 'std': std})
                    g.add_edge(edge[0], edge[1])
                else:
                    continue
            else:
                continue
        #对该树所有砍边的结果排序，并选择标准差最小的为切割结果
        cut_edges.sort(key=lambda x: x['std'])
        select_cut_edge = cut_edges[0]['edge']
        g.remove_edge(select_cut_edge[0],select_cut_edge[1])
        sub_graphs = nx.connected_component_subgraphs(g)

        for sub in sub_graphs:
            edges = sub.edges()
            nodes = sub.nodes()
            std = np.std(values[nodes])
            if len(nodes) <= 4:
                trees.append({'std': float('-inf'), 'nodes': nodes, "edges": edges})
            else:
                if len(trees) == 0:
                    trees.append({'std': std, 'nodes': nodes, "edges": edges})
                else:
                    for i in range(len(trees)):
                        if std > trees[i]['std']:
                            trees.insert(i, {'std': std, 'nodes': nodes, "edges": edges})
                            break
                    else:
                        trees.append({'std': std, 'nodes': nodes, "edges": edges})
        return cut_tree(trees, values, n_cluster)
    else:
        return trees


""" 根据类别重新构造数据 """
def add_label(data,trees):
    """
    :param data: 原始数据 [{}...]
    :param trees: 最终的分类树 [{'nodes':[...],'std':float,'edges':[[]...]}]
    :return: 添加了聚类标签的原始数据
    """
    for i in range(len(trees)):
        for node in trees[i]['nodes']:
            data[node]['vLabel'] = i
    return data


""" K-Means 预处理 """
def pre_cluster(points, k=40):
    estimator = KMeans(n_clusters=k).fit(points)
    labels = estimator.labels_
    clusters = []
    indexs = []
    for _ in range(k):
        clusters.append([])
        indexs.append([])
    for i in range(len(labels)):
        clusters[labels[i]].append(points[i])
        indexs[labels[i]].append(i)
    return clusters, indexs


def group_min_spaning_tree(data, n_cluster, init_cluster=20):
    points = []
    values = []
    for i in range(len(data)):
        points.append([data[i]['lat'],data[i]['lng']])
        values.append(data[i]['value'])
    values = np.array(values)

    clusters, indexs = pre_cluster(points, init_cluster)
    trees = []
    for i in range(init_cluster):
        if len(clusters[i]) >=4:
            g = create_delaunay(clusters[i], indexs[i])
            init_tree_edges, init_tree_nodes = init_min_spaning_tree(g)
            std = np.std(values[indexs[i]])
            trees.append({'edges': init_tree_edges, 'nodes':init_tree_nodes, 'std': std})
    trees.sort(key=lambda x: x['std'], reverse=True)
    return add_label(data, cut_tree(trees, values, n_cluster))


if __name__ == "__main__":
    import json

    start = time.time()
    with open('../data/Occupation.json', 'r') as fr:
        data = json.load(fr)
    data = group_min_spaning_tree(data, 800, init_cluster=100)
    with open('../data/Occupation_selectNodes.json', 'w') as fw:
        json.dump(data, fw)
    end = time.time()
    print(str(end - start))
