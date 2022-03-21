from sklearn.cluster import KMeans
import numpy as np

class HKeans:
    def __init__(self,n_clusters,height):
        self.n_clusters=n_clusters
        self.height=height
        self.gap=int((n_clusters-1)/(height-1))
    def kmeans(self,points,*n_clusters):
        if n_clusters==():
            n_clusters=self.n_clusters
        else:
            n_clusters=n_clusters[0]
        print(n_clusters)
        clusters=KMeans(n_clusters=n_clusters).fit(points).labels_
        return clusters


    def hierarchical(self,points):
        classCount=0
        classes = {}
        for i in range(self.height-1):
            if i==0:
                n_clusters=self.n_clusters
            else:
                if self.n_clusters==9 and i==1:
                    n_clusters=4
                elif self.n_clusters==9 and i==2:
                    n_clusters = 2
                else:
                    n_clusters=int(len(points)*0.4)
            clusters=self.kmeans(points,n_clusters)
            points_ = [[] for i in range(n_clusters)]
            for j in range(len(clusters)):
                point = [points[j][0], points[j][1], j]
                points_[clusters[j]].append(point)
            points.clear()
            for j in range(len(points_)):
                if classCount == 0:
                    classes[j] = {"id":j,"pointIndex": [k[2] for k in points_[j]]}
                else:
                    classes[j+classCount] = {"id":j+classCount,"children": [k[2]+classCount-len(clusters) for k in points_[j]]}
                p=np.array(points_[j])
                mean=np.mean(p,axis=0)
                points.append(mean.tolist()[:2])

            classCount+=n_clusters
        clusters=[0 for i in points]
        points_ = [[]]
        for j in range(len(clusters)):
            point = [points[j][0], points[j][1], j]
            points_[clusters[j]].append(point)
        classes[classCount]={"id":classCount,"children": [k[2]+classCount-len(clusters) for k in points_[0]]}
        print(classCount+1)
        # print(classes)
        return self.generteTree(classes,classCount)

    ##生成聚类树
    def generteTree(self, classes, root):

        subTree = {'id': root}
        if 'children' in classes[root]:
            subTree["children"] = []
            for i in classes[root]['children']:
                subTree["children"].append(self.generteTree(classes, i))
        else:
            subTree["pointIndex"] = classes[root]['pointIndex']
        return subTree

if __name__=="__main__":
    import json
    points = []
    fileName="Occupation"
    count=1000
    height=4
    with open('../data/' + fileName + '.json', 'r') as fr:
        Data = json.load(fr)
        for i in Data:
            points.append([i['lat'], i['lng']])
    tree=HKeans(n_clusters=count,height=height).hierarchical(points)
    with open(f'../data/{fileName}_tree_{count}_{height}.json','w') as fw:
        json.dump(tree,fw)