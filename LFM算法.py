import random

from example import Predict

#负样本采样
def RandomSelectNegativeSample(items,items_pool={}):
    ret = {}
    for i in items.keys():
        ret[i] = 1
        n = 0
        for i in range(len(items)*3):
            item = items_pool[random.randint(0,len(items_pool)-1)]
            if item in ret:
                continue
            ret[item] = 0
            n += 1
            if n > len(items):
                break
    return ret

def initModel(a,b):
    pass

#优化损失函数
def LatentFactorMode(users_items,F,N,alpha,lambd):
    [P,Q] = initModel(users_items,F)
    for step in range(N):
        for user,items in users_items.items():
            samples = RandomSelectNegativeSample(items)
            for item,rui in samples.items():
                eui = rui - Predict(user,item)
                for f in range(F):
                    P[user][f] += alpha * (eui * Q[item][f] - lambd * P[user][f])
                    Q[item][f] += alpha * (eui * P[user][f] - lambd * Q[item][f])
        alpha *= 0.9

def Recommend(user,P,Q):
    rank = {}
    for f,puf in random(len(P[user])):
        for i,qfi in Q[f]:
            if i not in rank:
                rank[i] = Predict(user,i)
    return rank
