import numpy as np
from flask import Flask, request, jsonify, make_response
import json
from jenkspy import JenksNaturalBreaks
from sampling.sample_bns import apply_bns
from sampling.sample_super import apply_super_bns
import random
from sklearn.cluster import KMeans

globalConfig = {'jnb': None, 'values': [], 'hull': []}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


@app.route("/upload_file", methods=['POST'])
def upload_file():
    file = request.files.get('file')
    res = make_response(jsonify({'code': 200, 'data': file.read().decode()}))
    return res


@app.route("/get_origin_data", methods=['POST'])
def get_origin_data():
    file_name = request.get_json()['fileName']
    with open(f'./data/{file_name}.json', 'r') as fr:
        data = json.load(fr)
    # points = []
    values = []
    for i in data:
        # points.append([i['lng'], i['lat']])
        values.append(i['value'])
    globalConfig['values'] = values
    # shape = alphashape.alphashape(points, 15)
    # hull = [[x, y] for x, y in shape.exterior.coords]
    hull = []
    out = {'data': data, 'hull': hull}
    globalConfig['hull'] = hull
    res = make_response(jsonify({'code': 200, 'data': out}))
    return res


@app.route("/get_cluster_data", methods=['POST'])
def get_cluster_data():
    values = request.get_json()['originData']
    n_cluster = request.get_json()['n_cluster']
    method = request.get_json()['method']
    labels = []
    if method == 'K-Means':
        km = KMeans(n_clusters=n_cluster).fit(np.array(values).reshape(-1, 1))
        labels = [int(i) for i in km.labels_]
    elif method == 'N-Breaks':
        jnb = JenksNaturalBreaks(nb_class=n_cluster)
        jnb.fit(values)
        labels = [int(i) for i in jnb.labels_]
    print(labels)
    res = make_response(jsonify({'code': 200, 'data': {'labels': labels}}))
    return res


@app.route("/bns_sampling", methods=['POST', 'GET'])
def bns_sampling():
    if request.method == 'POST':
        file_name = request.get_json()['fileName']
        r = request.get_json()['rate']
        flag = request.get_json()['flag']
        n_cluster = request.get_json()['n_cluster']
        if flag:
            with open(f'./data/{file_name}$class={n_cluster}.json', 'r') as fr:
                data = json.load(fr)
            data_dic = {i['id']: i['label'] for i in data}
            with open(f'./data/bns_{file_name}$rate={r}$count=0.json') as fr:
                data_processed = json.load(fr)
                rate = r
                for i in range(len(data_processed)):
                    data_processed[i]['label'] = data_dic[data_processed[i]['id']]
                # for i in range(len(data_processed)):
                #     data_processed[i]['label'] = globalConfig['jnb'].predict(data_processed[i]['value'])
        else:
            data_processed, bns = apply_bns(file_name, r)
            rate = bns.rate
        res = make_response(jsonify({'code': 200, 'data': data_processed, 'rate': rate}))
    return res


@app.route("/super_bns_sampling", methods=['POST', 'GET'])
def super_bns_sampling():
    if request.method == 'POST':
        file_name = request.get_json()['fileName']
        r = request.get_json()['rate']
        n_cluster = request.get_json()['n_cluster']
        min_r = request.get_json()['min_r']
        flag = request.get_json()['flag']
        if flag:
            with open(f'./data/zdhxbns1_{file_name}$class={n_cluster}$rate={r}$min_r={min_r}$count=0.json') as fr:
                data_processed = json.load(fr)
                rate = r
                # for i in range(len(data_processed)):
                #     data_processed[i]['label'] = globalConfig['jnb'].predict(data_processed[i]['value'])
        else:
            data_processed, bns = apply_super_bns(file_name, r)
            rate = bns.rate
        res = make_response(jsonify({'code': 200, 'data': data_processed, 'rate': rate}))
    return res


@app.route("/random_sampling", methods=['POST', 'GET'])
def random_sampling():
    if request.method == 'POST':
        file_name = request.get_json()['fileName']
        rate = request.get_json()['rate']
        n_cluster = request.get_json()['n_cluster']
        with open(f'./data/{file_name}.json', 'r') as fr:
            data = json.load(fr)
        count = int(len(data) * rate)
        data_processed = random.sample(data, count)
        with open(f'./data/{file_name}$class={n_cluster}.json', 'r') as fr:
            data = json.load(fr)
        data_dic = {i['id']: i['label'] for i in data}
        for i in range(len(data_processed)):
            data_processed[i]['label'] = data_dic[data_processed[i]['id']]
        res = make_response(jsonify({'code': 200, 'data': data_processed, 'rate': rate}))
    return res


@app.route("/create_sampling_color_label", methods=['POST', 'GET'])
def create_sampling_color_label():
    if request.method == 'POST':
        values = request.get_json()['values']
        n_cluster = request.get_json()['n_cluster']
        if n_cluster > 0:
            jnb = JenksNaturalBreaks(nb_class=n_cluster)
            # case 1,2用
            jnb.fit(globalConfig['values'])
            # 一般时候用
            # jnb.fit(values)
            print(jnb.breaks_)
            labels = [int(jnb.predict(i)) for i in values]
        else:
            labels = [0 for i in values]
        res = make_response(jsonify({'code': 200, 'data': labels}))
    return res


@app.route("/shape_optimization", methods=['POST', 'GET'])
def shape_optimization():
    if request.method == 'POST':
        file_name = request.get_json()['fileName']
        r = request.get_json()['rate']
        n_cluster = request.get_json()['n_cluster']
        flag = request.get_json()['flag']
        min_r = request.get_json()['min_r']
        knn = request.get_json()['knn']
        if flag:
            with open(f'./data/zdhxbns1_{file_name}$class={n_cluster}$rate={r}$min_r={min_r}$count=0$knn={knn}.json') as fr:
                data_processed = json.load(fr)
                rate = r
                print(r, len(data_processed))
        res = make_response(jsonify({'code': 200, 'data': data_processed, 'rate': rate}))
    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=5000)
