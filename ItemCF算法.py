import math
from operator import itemgetter

#物品相似度
def ItemSimilarity(train):
    C,N = {},{}
    for users,items in train.items():
        for i in users:
            N[i] += 1
            for j in users:
                if i == j:
                    continue
                C[i][j] += 1

    W = {}
    for i,related_items in C.items():
        for j,cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    return W

#itemCF
def Recommendation(train,user_id,W,K):
    rank = {}
    ru = train[user_id]
    for i,pi in ru.items():
        for j,wj in sorted(W[i].items(),key=itemgetter(1),reverse=True)[0:K]:
            if j in ru:
                continue
            rank[j] += pi*wj
    return rank

#改进版物品相似度itemCF-IUF
def ItemSimilarity2(train):
    C,N = {},{}
    for users,items in train.items():
        for i in users:
            N[i] += 1
            for j in users:
                if i == j:
                    continue
                C[i][j] += 1 / math.log(1+len(items)*1.0)  #唯一差别

    W = {}
    for i,related_items in C.items():
        for j,cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    return W
