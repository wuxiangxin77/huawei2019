import numpy as np
from math import sqrt
inf = 999999

# 创建邻接矩阵
def floyd(data_road, data_cross, crossId, flag, flag2):
    cross_num = len(data_cross)
    adj = np.empty([cross_num, cross_num], dtype='int32')
    adj.fill(inf)
    # 对角线值为0
    for num in range(cross_num):
        adj[num][num] = 0
    # 路口Id到index映射
    id2index = dict()
    for index in range(cross_num):
        id2index[data_cross[index].crossId] = index
    for data in data_road:

        if data.isDuplex == '1':
            if flag == 0:
                if data.laneNum > 3:
                    adj[id2index[data.startId]][id2index[data.endId]] = 24 / (sqrt(data.roadLength + data.maxSpeed) * data.laneNum)
                    adj[id2index[data.endId]][id2index[data.startId]] = 24 / (sqrt(data.roadLength + data.maxSpeed) * data.laneNum)
                else:
                    if flag2 == 0:
                        adj[id2index[data.startId]][id2index[data.endId]] = 40 / ( sqrt(data.roadLength + data.maxSpeed) * data.laneNum * data.laneNum)
                        adj[id2index[data.endId]][id2index[data.startId]] = 40 / (sqrt(data.roadLength + data.maxSpeed) * data.laneNum * data.laneNum)
                    else:
                        adj[id2index[data.startId]][id2index[data.endId]] = 30 / (sqrt(data.roadLength + data.maxSpeed) * data.laneNum)
                        adj[id2index[data.endId]][id2index[data.startId]] = 30 / (sqrt(data.roadLength + data.maxSpeed) * data.laneNum)
            else:
                if data.laneNum > 3:
                    adj[id2index[data.startId]][id2index[data.endId]] = 24 / (sqrt(data.roadLength) * data.laneNum)
                    adj[id2index[data.endId]][id2index[data.startId]] = 24 / (sqrt(data.roadLength) * data.laneNum)
                else:
                    if flag2 == 0:
                        adj[id2index[data.startId]][id2index[data.endId]] = 40 / (sqrt(data.roadLength) * data.laneNum * data.laneNum)
                        adj[id2index[data.endId]][id2index[data.startId]] = 40 / (sqrt(data.roadLength) * data.laneNum * data.laneNum)
                    else:
                        adj[id2index[data.startId]][id2index[data.endId]] = 30 / (sqrt(data.roadLength) * data.laneNum)
                        adj[id2index[data.endId]][id2index[data.startId]] = 30 / (sqrt(data.roadLength) * data.laneNum)

        else:
            if flag == 0:
                if data.laneNum > 3:
                    adj[id2index[data.startId]][id2index[data.endId]] = 40 / (sqrt(data.roadLength + data.maxSpeed) * data.laneNum)
                else:
                    if flag2 == 0:
                        adj[id2index[data.startId]][id2index[data.endId]] = 60 / ( sqrt(data.roadLength + data.maxSpeed) * data.laneNum * data.laneNum)
                    else:
                        adj[id2index[data.startId]][id2index[data.endId]] = 50/ (sqrt(data.roadLength + data.maxSpeed) * data.laneNum)
            else:
                if data.laneNum > 3:
                    adj[id2index[data.startId]][id2index[data.endId]] = 40 / (sqrt(data.roadLength) * data.laneNum)
                else:
                    if flag2 == 0:
                        adj[id2index[data.startId]][id2index[data.endId]] = 60 / (sqrt(data.roadLength) * data.laneNum * data.laneNum)
                    else:
                        adj[id2index[data.startId]][id2index[data.endId]] = 50 / (sqrt(data.roadLength) * data.laneNum)
            # else:
            #     adj[id2index[data.startId]][id2index[data.endId]] = 100 / (data.roadLength + data.maxSpeed)
    if crossId != '':
        id = crossId.split('_')
        adj[id2index[id[0]]][id2index[id[1]]] += adj[id2index[id[0]]][id2index[id[1]]]
    # 创建路径矩阵
    path = np.array([range(cross_num)])
    for i in range(cross_num - 1):
        path = np.append(path, [range(cross_num)], axis=0)
    # 求最短路径
    for i in range(cross_num):
        for j in range(cross_num):
            for k in range(cross_num):
                if adj[j][k] > adj[j][i] + adj[i][k]:
                    adj[j][k] = adj[j][i] + adj[i][k]
                    path[j][k] = path[j][i]
    return path, id2index


def shortest_path(data_cross, path, start_index, end_index):
    temp_path = path[start_index][end_index]
    min_path = list()
    min_path.append(data_cross[start_index].crossId)
    while temp_path != end_index:
        min_path.append(data_cross[temp_path].crossId)
        temp_path = path[temp_path][end_index]
    min_path.append(data_cross[temp_path].crossId)
    return min_path
