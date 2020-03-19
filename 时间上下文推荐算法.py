import math
from operator import itemgetter

def addToDict(a,b,c):
    pass

#物品最近流行度
def RecentPopularity(records,alpha,T):
    ret = {}
    for user,item ,tm in records:
        if tm >= T:
            continue
        addToDict(ret,item,1/(1.0+alpha*(T-tm)))
    return ret

#时间上下文相关的ItemCF算法

#ItemCF的相似度
def ItemSimilarity(train,alpha):
    C,N = {},{}
    for u,items in train.items():
        for i,tui in items.items():
            N[i] += 1
            for j,tuj in items.items():
                if i == j:
                    continue
                C[i][j] += 1/(1+alpha*abs(tui-tuj))
    W = {}
    for i,realted_items in C.items():
        for j,cij in realted_items.items():
            W[i][j] = cij/math.sqrt(N[i]*N[j])
    return W

def Recommendation(train,user_id,W,K,t0,alpha,tuj):
    rank ={}
    ru = train[user_id]
    for i,pi in ru.items():
        for j,wj in sorted(W[i].items(),key=itemgetter(1),reverse=True)[:K]:
            if (j,tuj) in ru.items():
                continue
            rank[j] += pi*wj / (1+alpha*(t0-tuj))
    return rank

#时间上下文相关的UserCF算法

#UserCF的相似度
def UserSimilarity(train,alpha):
    item_users = {}
    for u,items in train.items():
        for i,tui in items.items():
            if i not in item_users:
                item_users[i] = {}
            item_users[i][u] = tui
    C,N = {},{}
    for i,users in item_users.items():
        for u,tui in users.items():
            N[u] += 1
            for v,yvi in users.items():
                N[u] += 1
                for v,tvi in users.items():
                    if u == v:
                        continue
                    C[u][v] += 1/(1+alpha*abs(tui-tvi))
    W = {}
    for u,related_users in C.items():
        for v,cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u]*N[v])
    return W

def Recommend(user,T,train,W,K,alpha):
    rank = {}
    interacted_items = train[user]
    for v,wuv in sorted(W[user].items(),key=itemgetter(1),reverse=T)[:K]:
        for i,tvi in train[v].items():
            if i in interacted_items:
                continue
            rank[i] += wuv / (1+alpha*(T-tvi))
    return rank

#路径融合算法
def PathFusion(user,time,G,alpha):
    Q,V,depth,rank = [],set(),{},{}
    depth['u:'+user] = 0
    depth['ut:'+user+"_"+time] = 0
    rank['u:'+user] = alpha
    rank['ut:'+user+"_"+time] = 1-alpha
    Q.append('u:'+user)
    Q.append('ut:'+user+"_"+time)
    while len(Q) > 0:
        v = Q.pop()
        if v in V:
            continue
        if depth[v] > 3:
            continue
        for v2,w in G[v].items():
            if v2 not in V:
                depth[v2] = depth[v] + 1
                Q.append(v2)
            rank[v2] = rank[v] * w
    return rank