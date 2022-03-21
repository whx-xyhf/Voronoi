import math
import numpy as np
from scipy.spatial import Delaunay
from sklearn.cluster import KMeans


ENV_DEV = False


""" K-Means 预处理 """
def pre_cluster(points, k=40):
  X = np.array([[p[1], p[2]] for p in points])
  estimator = KMeans(n_clusters=k).fit(X)
  labels = estimator.labels_
  clusters = [[] for _ in range(k)]
  for point, label in zip(points, labels):
    clusters[label].append(point)
  return clusters


""" 将点连接为最小生成树 """
def connect_nodes(points, num):
  points, extend = normalize_values(points)
  
  map_id_to_node = {}
  
  for point in points:
    _id, x, y, val = point
    map_id_to_node[_id] = {
      "x":  x,
      "y":  y,
      "v":  val
    }

  print("performing pre-clustering using KMeans...")
  clusters = pre_cluster(points, k=int(num / 16))
  print("generated {} clusters".format(len(clusters)))

  trees = []
  s = 0

  for cluster in clusters:
    print("generating MST... ({}/{})".format(len(trees), len(clusters)))
    tri = Delaunay(np.array(
      [[p[1], p[2]] for p in cluster]
    ))

    links = []

    for simplice in tri.simplices:
      for edge in [[0, 1], [0, 2], [1, 2]]:
        pid_a = cluster[simplice[edge[0]]][0]
        pid_b = cluster[simplice[edge[1]]][0]
        pid_a, pid_b = min(pid_a, pid_b), max(pid_a, pid_b)
        pa = map_id_to_node[pid_a]
        pb = map_id_to_node[pid_b]
        w = abs(pa["v"] - pb["v"])
        links.append((pid_a, pid_b, w))

    mst = kruskal(links)
    s += len(mst["nodes"])
    trees.append(mst)

  print("start prunning...")

  trees = prun(map_id_to_node, trees, num)

  map_id_to_tree = {}

  for t, tree in enumerate(trees):
    for node in tree["nodes"]:
      map_id_to_tree[node] = t

  return map_id_to_tree


""" Kruskal 算法 - 最小生成树 """
def kruskal(links):
  tree = {
    "nodes":  [],
    "links":  []
  }
  where_is_node = {}
  flag = 0
  _links = sorted(links, key=lambda l : l[2])
  for link in _links:
    a, b = link[0], link[1]
    wia = where_is_node[a] if a in where_is_node else -1
    wib = where_is_node[b] if b in where_is_node else -1
    if wia == wib == -1:
      flag += 1
      where_is_node[a] = flag
      where_is_node[b] = flag
      tree["nodes"] += [a, b]
      tree["links"].append({
        "source": min(a, b),
        "target": max(a, b)
      })
    elif wia == wib:
      continue
    elif wib == -1:
      where_is_node[b] = wia
      tree["nodes"].append(b)
      tree["links"].append({
        "source": min(a, b),
        "target": max(a, b)
      })
    elif wia == -1:
      where_is_node[a] = wib
      tree["nodes"].append(a)
      tree["links"].append({
        "source": min(a, b),
        "target": max(a, b)
      })
    else:
      for nid in where_is_node:
        if where_is_node[nid] == wib:
          where_is_node[nid] = wia
      tree["links"].append({
        "source": min(a, b),
        "target": max(a, b)
      })

  return tree


""" 切割树 """
def prun(nodes, trees, num):
  trees_with_cost = []

  for tree in trees:
    trees_with_cost.append({
      "nodes":  tree["nodes"],
      "links":  tree["links"],
      "cost":   None
    })

  n_op, step = num - len(trees_with_cost), 0
  while len(trees_with_cost) < num:
    # 选择类内差距最大的将其拆分
    _max, _idx = 0, 0
    for i, tree in enumerate(trees_with_cost):
      if tree["cost"] == None:
        # 计算代价
        cost = std([nodes[j]["v"] for j in tree["nodes"]])
        tree["cost"] = cost
      if len(tree["nodes"]) > 1 and tree["cost"] > _max:
        _max = tree["cost"]
        _idx = i
    tree_to_prun = trees_with_cost.pop(_idx)
    # 找出最适合的拆分
    _min = None
    next_cut = [None, None]
    for i in range(len(tree_to_prun["links"])):
      # 迭代移除一条边
      use_links = [link for j, link in enumerate(tree_to_prun["links"]) if j != i]
      tree_a, tree_b = tree_cut(tree_to_prun["nodes"], use_links)
      # 计算新的代价（最大值）
      cost_a = std([nodes[j]["v"] for j in tree_a["nodes"]])
      cost_b = std([nodes[j]["v"] for j in tree_b["nodes"]])
      tree_a["cost"] = cost_a
      tree_b["cost"] = cost_b
      cost = max(cost_a, cost_b)
      if _min == None or cost < _min:
        _min = cost
        next_cut = [tree_a, tree_b]
    # 应用切割
    trees_with_cost.append(next_cut[0])
    trees_with_cost.append(next_cut[1])
    if ENV_DEV:
      print("\r" * 100 + "{}/{} --- cut {} into {}+{}".format(
        len(trees_with_cost), num,
        len(tree_to_prun["nodes"]), len(next_cut[0]["nodes"]), len(next_cut[1]["nodes"])
      ))
      # print("prunning... {:.2%}".format(step / n_op))
    else:
      print("prunning... {:.2%}".format(step / n_op))
    step += 1
    pass
  return trees_with_cost


""" 构建切割后的树 """
def tree_cut(nodes, links):
  if len(nodes) == 2:
    return [{
      "nodes":  [nodes[0]],
      "links":  [],
      "cost":   None
    }, {
      "nodes":  [nodes[1]],
      "links":  [],
      "cost":   None
    }]

  _links = [link for link in links]
  _nodes = [node for node in nodes]
  groups = []
  for link in _links:
    a, b = link["source"], link["target"]
    wia, wib = -1, -1
    for i, grp in enumerate(groups):
      if a in grp["nodes"]:
        wia = i
      if b in grp["nodes"]:
        wib = i
    if wia == wib == -1:
      groups.append({
        "nodes":  [a, b],
        "links":  [link],
        "cost":   None
      })
    elif wib == -1:
      groups[wia]["nodes"].append(b)
      groups[wia]["links"].append(link)
    elif wia == -1:
      groups[wib]["nodes"].append(a)
      groups[wib]["links"].append(link)
    elif wia == wib:
      if ENV_DEV:
        print("error", wia, wib, groups)
    else:
      grp_a = groups[wia]
      grp_b = groups.pop(wib)
      grp_a["nodes"] += grp_b["nodes"]
      grp_a["links"] += grp_b["links"]
      grp_a["links"].append(link)
  if len(groups) == 1:
    groups.append({
      "nodes":  [node for node in _nodes if node not in groups[0]["nodes"]],
      "links":  [],
      "cost":   None
    })
  tree_a = groups[0]
  tree_b = groups[1]
  
  return tree_a, tree_b


""" 计算均值 """
def std(array):
  mean = 0
  for d in array:
    mean += d
  mean /= len(array)
  std = 0
  for d in array:
    std += (d - mean) ** 2
  # TODO 这里把总数开了个根号，尝试让数量大的更容易被划分
  # （接上条）还是算了
  # std = (std / len(array) ** 0.5) ** 0.5
  std = (std / len(array)) ** 0.5
  return std


""" 归一化属性值 """
def normalize_values(points):
  _min = _max = points[0][3]
  _minLng = _maxLng = points[0][1]
  _minLat = _maxLat = points[0][2]
  for point in points[1:]:
    if point[3] > _max:
      _max = point[3]
    if point[3] < _min:
      _min = point[3]
    if point[1] > _maxLng:
      _maxLng = point[1]
    if point[1] < _minLng:
      _minLng = point[1]
    if point[2] > _maxLat:
      _maxLat = point[2]
    if point[2] < _minLat:
      _minLat = point[2]
  for point in points:
    point[3] = (point[3] - _min) / (_max - _min)
  
  return points, ((_minLng, _maxLng), (_minLat, _maxLat))
