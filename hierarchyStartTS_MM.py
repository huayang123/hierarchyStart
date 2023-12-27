import random
from pylab import *
import matplotlib as mpl
import networkx as nx
from matplotlib import pyplot as plt
import math
import matplotlib.pyplot as plt
from matplotlib import font_manager
import random
import itertools
import datetime


def ShowGraph(glists, ginfo, rowsize=3):
    row = ceil(len(glists) / rowsize)
    plt.subplots(int(row), rowsize, figsize=(18, 25))

    for ind in range(len(glists)):
        plt.subplot(row, rowsize, ind + 1)
        nx.draw(glists[ind], with_labels=True, font_weight='bold')
        myfont = font_manager.FontProperties(fname='C:\Windows\Fonts\STFANGSO.TTF', size=6)
        plt.title(ginfo[ind], fontproperties=myfont)
        plt.axis('on')
        plt.xticks([])
        plt.yticks([])
    plt.gcf().subplots_adjust(left=0.01,right=0.99,top=0.99,bottom=0.01)
    plt.show()

start=datetime.datetime.now()
graph = "Hsn"
print(graph)
n = input("n=")
n = int(n)

bh = []
p = math.factorial(n)
q = int(math.pow(p, 2))

for i in range(0, q):
    bh.append(tuple(('', '')))
nums = []
for k in range(1, n + 1):
    nums.append(k)
i = 0

for num in itertools.permutations(nums, n):
    a = ''
    for m in range(n):
        a = a + str(num[m])
    for num in itertools.permutations(nums, n):
        b = ''
        for m in range(n):
            b = str(b) + str(num[m])
        c = (a, b)
        bh[i] = c
        i = i + 1


mmm = n*(n-1)/2-1
mmm=int(mmm)
print(f'故障节点上限是{mmm}')
faultNumber=random.randint(0,mmm)
print(f'随机找的故障节点的个数{faultNumber}')
xbh = []
xbh = random.sample(bh, faultNumber)
keys = bh
values = []
for u in range(len(keys)):
    values.append(0)
for i in range(faultNumber):
    for u in range(len(keys)):
        if keys[u] == xbh[i]:
            values[u] = 1
dictionary = {}
for i in range(len(keys)):
    x = int(values[i])
    dictionary.setdefault(keys[i], []).append(x)

def drawing(G,theList):
    q=len(theList)
    for u in range(q - 1):  # u和v属于同一个子模块，而且u的位置编号和v的位置编号在Sn中是相邻
        theSecondUnit = str(theList[u][1])
        neighbor = []
        single = []
        for k in range(n):  # 获得第二维编号的所有单个数字，方便后续交换数字位置找邻居
            valueOfSingle = theSecondUnit[k]
            single.append(valueOfSingle)
        for g in range(1, len(single)):  # 这里找u的模块内部边是按照节点的数字置换关系找的，但是找到一个邻居之后还需要在原来未曾处理过的数字上再置换
            theSingle = single[:]  # 创造一个暂时的数组进行数字置换操作
            swamp = theSingle[0]
            theSingle[0] = theSingle[g]
            theSingle[g] = swamp
            secondDu = "".join(theSingle)  # 把u的所有邻居v的二维位置列表转化成字符串
            newNode = (theList[u][0], secondDu)
            neighbor.append(newNode)
        for v in range(u + 1, q):
            for ss in range(0, len(neighbor)):
                if theList[v][0] == theList[u][0] and theList[v][1] == neighbor[ss][1]:
                    G.add_edge(theList[u], theList[v])  # 不会重复添加边的

    single = []
    theSingle = []
    for u in range(q - 1):  # u和v不在同一个Sn模块中，但是每个顶点的自身模块编号和位置编号一致并且相互之间互为倒序排列
        if theList[u][0] == theList[u][1]:
            theUnit = str(theList[u][1])
            single = []
            for k in range(n):  # 获得u节点编号的所有单个数字，方便后续交换数字位置找邻居
                valueOfSingle = theUnit[k]
                single.append(valueOfSingle)
            theSingle = single[:]
            for g in range(math.floor(len(single) / 2)):
                swamp = theSingle[g]
                theSingle[g] = theSingle[n - 1 - g]
                theSingle[n - 1 - g] = swamp
            theDu = "".join(theSingle)  # 把获得的字符数组转化成字符串

            for v in range(u + 1, q):  # 在全图中寻找u的邻居节点
                if theList[v][0] == theList[u][0]:
                    continue
                if theList[v][1] == theList[v][0] and theList[v][0] == theDu:
                    G.add_edge(theList[u], theList[v])  # 不会重复添加边的

    single = []
    theSingle = []
    for u in range(q - 1):  # u和v不在同一个模块中，但是u顶点的模块编号与v顶点的位置编号一致，并且同样的v顶点的模块编号与u顶点的位置编号一致
        for v in range(u + 1, q):
            if theList[u][0] != theList[v][0]:
                if theList[u][0] == theList[v][1] and theList[u][1] == theList[v][0]:
                    G.add_edge(theList[u], theList[v])
    return G

G1 = nx.Graph()
G1.add_nodes_from(bh)
G1=drawing(G1,bh)

def bfs(node, wgz, gzqueue):
    if node is None:
        return
    queue = []
    nodeSet = set()
    nodeSet.add(node)
    queue.append(node)
    wgz.append(node)
    while len(queue) > 0:
        cur = queue.pop(0)
        for i in range(0, len(G1.adj[cur]), 1):  # 在Hsn中每个节点都有n个邻居节点
            xx = list(G1.adj[cur])[i]  # 把获得的cur节点的所有邻居的字典转化成列表类型并取出第i位即第一个邻居
            if xx not in nodeSet:
                for j in range(0, len(G1.adj[xx]), 1):
                    yy = list(G1.adj[xx])[j]
                    if dictionary[cur] == dictionary[xx] and dictionary[xx] == dictionary[yy]: #MM*的比较方式
                        queue.append(xx)
                        nodeSet.add(list(G1.adj[cur])[i])
                        wgz.append(xx)
                        break
                    if j == n - 1 and xx not in gzqueue:  # 当cur的节点xx不满足条件时候，就是故障节点
                        gzqueue.append(xx)


wgz = []
gzqueue = []
wgz1 = []
gzqueue1 = []
for se in range(q - 1):
    x = list(G1.nodes)[se]
    bfs(x, wgz, gzqueue)
    if (len(wgz) > len(wgz1)):
        wgz1 = []
        gzqueue1 = []
        wgz1 = wgz
        gzqueue1 = gzqueue
        se1 = x
    wgz = []
    gzqueue = []
wgz = wgz1
gzqueue = gzqueue1
print(f'gzqueue={gzqueue}')


G2 = nx.Graph()
G2.add_nodes_from(wgz)
G2=drawing(G2,wgz)
print(G2.node)

czcgz = []
youle = []
if dictionary[x] == [0]:  # 以x节点为起始节点
    for u in range(len(bh) - 1):
        for v in range(len(bh)):
            if not G2.has_node(bh[u]):
                break
            else:
                if G1.has_edge(bh[u], bh[v]) and bh[v] not in G2[bh[u]] and bh[v] not in youle:
                    youle.append(bh[v])
                    czcgz.append(bh[v])



G3 = nx.Graph()
G3.add_nodes_from(czcgz)
G3=drawing(G3,czcgz)

G4 = nx.Graph()
zcz = xbh
G4.add_nodes_from(zcz)
G4=drawing(G4,zcz)

end=datetime.datetime.now()
print('Running time: %s Seconds'%(end-start))

glists = [G2, G3, G4]
if len(wgz) >= mmm:
    ginfo = [f'The maximum number of connected component is {len(wgz)}, starting from node {x}',
             f'number of fault nodes diagnosed by Hsn is {len(czcgz)}',
             f'Diag {len(zcz)}']
else:
    ginfo = [
        f'Hs{n}Hsn structure starts from {x} node with breadth-first traversal，{x} is a fault node, so all nodes in the graph are fault nodes',
        f'NONE', f'NONE']
ShowGraph(glists, ginfo)
