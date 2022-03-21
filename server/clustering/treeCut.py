import numpy as np
import math
from jenkspy import JenksNaturalBreaks
import copy

class TreeCut:
    def __init__(self,tree,valList,n_clusters):
        # self.treeNodes={}
        process=self.calculateAttr(tree,np.array(valList),'val')
        self.tree=process[1]
        self.valList=process[2]
        self.n_clusters=n_clusters
        self.hierarchicalNodes={}
        self.jnb=self.attrClustering()
        self.maxHeight=None
        # self.labelDic=self.attrClustering()

    def calculateAttr(self,tree,valList,word):
        index=[]
        # self.treeNodes[tree["id"]] = tree
        if 'children' in tree:
            for i in tree['children']:
                result=self.calculateAttr(i, valList,word)
                index.extend(result[0])
                valList=result[2]
        else:
            index=tree["pointIndex"]
        val = valList[index]
        mean = np.mean(val)
        valList = np.append(valList, mean)
        tree[word] = mean
        return index,tree,valList

    def attrClustering(self):
        # labelDic={}
        jnb=JenksNaturalBreaks(nb_class=self.n_clusters)
        jnb.fit(self.valList)
        # labels=jnb.labels_
        # for i in range(len(labels)):
        #     labelDic[self.valList[i]]=labels[i]
        return jnb

    def IE(self,labelList):
        label=set(labelList)
        count=len(labelList)
        result=0
        for i in label:
            count_i=labelList.count(i)
            p_i=count_i/count
            result+=-p_i*math.log10(p_i)
        return result
    def CV(self,valList):
        valList=np.array(valList)
        std=np.std(valList)
        mean=np.mean(valList)
        if mean ==0:
            return 0
        return std/mean

    def addIe(self,tree):
        labels = []
        if "children" in tree:
            for i in range(len(tree["children"])):
                # labels.append(self.labelDic[tree["children"][i]["val"]])
                labels.append(self.jnb.predict(tree["children"][i]["val"]).tolist())
            ie = self.IE(labels)
            tree['ie2']=ie
            for i in range(len(tree["children"])):
                self.addIe(tree["children"][i])
        else:
            for i in tree["pointIndex"]:
                # labels.append(self.labelDic[self.valList[i]])
                labels.append(self.jnb.predict(self.valList[i]).tolist())
            tree['ie2']=self.IE(labels)
    def addCv(self,tree):
        valList = []
        if "children" in tree:
            for i in range(len(tree["children"])):
                valList.append(tree["children"][i]["val"])
            cv = self.CV(valList)
            tree['ie'] = cv
            for i in range(len(tree["children"])):
                self.addCv(tree["children"][i])
        else:
            for i in tree["pointIndex"]:
                valList.append(self.valList[i])
            tree['ie'] = self.CV(valList)

    def judge(self,tree,th_ie):
        selectNode=[]
        # labels=[]
        if "children" in tree:
            # for i in range(len(tree["children"])):
            #     labels.append(self.labelDic[tree["children"][i]["val"]])
            ie=tree['ie']
            if ie>th_ie:
                for i in range(len(tree["children"])):
                    selectNode.extend(self.judge(tree["children"][i],th_ie))
            else:
                selectNode.append(tree)
                # self.treeNodes[tree["id"]]['ie']=ie
            return selectNode
        else:
            # for i in tree["pointIndex"]:
            #     labels.append(self.labelDic[self.valList[i]])
            # ie = self.IE(labels)
            ie=tree['ie']
            if ie>th_ie:
                for i in tree["pointIndex"]:
                    selectNode.append({"index":i,"parent":tree["id"],"ie":0,"val":self.valList[i]})
            else:
                selectNode.append(tree)
                # self.treeNodes[tree["id"]]['ie'] = ie
            return selectNode

    def cutTree(self,tree,ids):
        if "children" in tree:
            if ids.count(tree['id']) > 0:
                del tree['children']
            else:
                for i in tree['children']:
                    self.cutTree(i,ids)

    def cut(self,th_ie):
        self.addCv(self.tree)

        selectNode=self.judge(self.tree,th_ie)
        self.selectNode=selectNode
        ids=[]
        for i in selectNode:
            if 'id' in i:
                ids.append(i['id'])
            else:
                ids.append(i['parent'])
        tree=copy.deepcopy(self.tree)
        self.cutTree(tree,ids)
        self.cTree=tree


    def getHeightPoints(self, lat=[], lng=[]):
        nodes = [self.tree]
        index = 0
        result = {}
        while len(nodes) > 0:
            temp = []
            index += 1
            nodes_ = copy.deepcopy(nodes)
            # print(index)
            while len(nodes_) > 0:
                nodes_.pop(0)
                j = nodes.pop(0)
                # print(len(nodes))
                if "children" in j:
                    for i in range(len(j["children"])):
                        nodes.append(j["children"][i])
                        temp.append(j["children"][i])
                else:
                    # print("!!!!!!!!!!!!!!!!!!!!",index,len(nodes))
                    # for i in range(len(j["pointIndex"])):
                    #     temp.append({"lat": lat[j["pointIndex"][i]], "lng": lng[j["pointIndex"][i]],
                    #                  "val": valList[j["pointIndex"][i]], "ie": 0})
                    for i in range(len(j["pointIndex"])):
                        temp.append({"val": self.valList[j["pointIndex"][i]], "ie": 0,"ie2":0,'index':j["pointIndex"][i],"lat": lat[j["pointIndex"][i]], "lng": lng[j["pointIndex"][i]]})
            result[index] = temp
            print(index,len(temp))
        return result,index

    def cut_bottom(self,th_ie,lat=[],lng=[]):
        hierarchicalNodes,maxHeight=self.getHeightPoints(lat=lat,lng=lng)
        self.maxHeight=maxHeight
        self.hierarchicalNodes=hierarchicalNodes
        print(maxHeight,hierarchicalNodes.keys())
        selectNodes=[]
        selectIds=[]
        bottomNode=[]
        for i in range(maxHeight-1,0,-1):
            count=0
            nodes=hierarchicalNodes[i]
            if i == maxHeight - 1:
                maxCv=max(nodes,key=lambda x:x['ie'])['ie']
                minCv=min(nodes,key=lambda x:x['ie'])['ie']
                th_ie=minCv+(maxCv-minCv)*th_ie
                print(maxCv,minCv,th_ie)
                for node in nodes:
                    if node['ie']<th_ie:
                        selectNodes.append(node)
                        selectIds.append(node['id'])
                        count+=1
                    else:
                        for j in range(len(node["pointIndex"])):
                            bottomNode.append({"index":node['pointIndex'][j],"parent":node["id"],"ie":0,"ie2":0,"val":self.valList[node['pointIndex'][j]]})
            else:
                for node in nodes:
                    if node ['ie']<th_ie:
                        isselect=True
                        condidateId=[]
                        for child in node['children']:
                            if selectIds.count(child['id'])==0:
                                isselect=False
                                break
                            else:
                                condidateId.append(child['id'])
                        if isselect:
                            for Id in condidateId:
                                index=selectIds.index(Id)
                                del selectNodes[index]
                                del selectIds[index]
                            selectNodes.append(node)
                            selectIds.append(node['id'])
                            count+=1

            print(str(i)+"层:select"+str(count)+"个")
        selectNodes.extend(bottomNode)
        self.selectNode=selectNodes
        print('selectNum:',len(selectNodes))
        ids = []
        for i in selectNodes:
            if 'id' in i:
                ids.append(i['id'])
            else:
                ids.append(i['parent'])
        tree = copy.deepcopy(self.tree)
        self.cutTree(tree, ids)
        self.cTree = tree
        return selectNodes


def getLeaves(tree):
    # self.treeNodes[tree["id"]] = tree
    children=[]
    if 'children' in tree:
        for i in tree['children']:
            children.extend(getLeaves(i))
    else:
        children=tree["pointIndex"]

    return children


if __name__=="__main__":
    import json
    fileName = "Occupation"
    count = 1000
    height = 4
    with open(f'../data/{fileName}_tree_{count}_{height}.json','r') as fr:
        tree=json.load(fr)
    with open(f'../data/{fileName}.json','r') as fr:
        data=json.load(fr)
    valList=[]
    lat=[]
    lng=[]
    for i in data:
        lat.append(i['lat'])
        lng.append(i['lng'])
        valList.append(i["value"])
    tc=TreeCut(tree,valList,10)
    tc.addCv(tc.tree)
    tc.calculateAttr(tc.tree, np.array(lat), 'lat')
    tc.calculateAttr(tc.tree, np.array(lng), 'lng')
    tc.cut_bottom(0.65, lat=lat, lng=lng)
    print(len(tc.selectNode))

    selectNodes=tc.selectNode
    count=len(selectNodes)
    for i in range(count):
        if 'pointIndex' in selectNodes[i]:
            for j in selectNodes[i]['pointIndex']:
                data[j]['vLabel']=i
        elif 'children' in selectNodes[i]:
            leaves=getLeaves(selectNodes[i])
            for j in leaves:
                data[j]['vLabel']=i
        else:
            data[selectNodes[i]['index']]['vLabel']=i

    with open(f'../data/{fileName}_selectNodes.json','w') as fw:
        json.dump(data,fw)