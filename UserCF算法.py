import math
import random
from operator import itemgetter

#用户相似度
def UserSimilarity(train):
    item_users = {}
    for u,items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    C,N = {},{}
    for i ,users in item_users.items():
        for u in users:
            N[u] += 1
            for v in users:
                if u ==v:
                    continue
                C[u][v] += 1

    W = {}
    for u,related_users in C.items():
        for v,cuv in related_users.items():
            W[u][v] = cuv/math.sqrt(N[u]*N[v])
    return W

#userCF
def Recommend(user,train,W,K=3):
    rank = {}
    interacted_items = train[user]
    for v,wuv in sorted(W[user].items,key=itemgetter(1),reverse=True)[0:K]:
        for i,rvi in train[v].items():
            if i in interacted_items:
                continue
            rank[i] += wuv*rvi
    return rank

#改进版用户相似度计算,userCF-IIF
def UserSimilarity2(train):
    item_users = {}
    for u,items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    C,N ={},{}
    for i,users in item_users.items():
        for u in users:
            N[u] += 1
            for v in users:
                if u == v:
                    continue
                C[u][v] += 1/math.log(1+len(users))  #唯一差别

    W ={}
    for u,related_users in C.items():
        for v,cuv in related_users.items():
            W[u][v] = cuv/math.sqrt(N[u]*N[v])
    return W

