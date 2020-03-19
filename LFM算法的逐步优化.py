import math
import random

#一开始未优化版
def InitLFM(train,F):
    p,q = {},{}
    for u,i,rui in train.items():
        if u not in p:
            p[u] = [random.random()/math.sqrt(x) for x in range(F)]
        if i not in q:
            q[i] = [random.random()/math.sqrt(x) for x in range(F)]
    return list([p,q])

def Predict(u,i,p,q):
    return sum([p[u][f]*q[i][f] for f in range(len(p[u]))])

def LearningLFM(train,F,n,alpha,lambd,k):
    [p,q] = InitLFM(train,F)
    for step in range(n):
        for u,i,rui in train.items():
            pui = Predict(u,i,p,q)
            eui = rui - pui
            for f in range(F):
                p[u][k] += alpha*(q[i][k]*eui - lambd*p[u][k])
                q[i][k] += alpha*(p[u][k]*eui-lambd*q[i][k])
        alpha *= 0.9
    return list([p,q])

#加了偏置的优化版
def InitBiasLFM(train,F):
    p,q,bu,bi = {},{},{},{}
    for u,i,rui in train.items():
        bu[u],bi[i] = 0,0
        if u not in p:
            p[u] = [random.random()/math.sqrt(x) for x in range(F)]
        if i not in q:
            q[i] = [random.random()/math.sqrt(x) for x in range(F)]
    return list([p,q,bu,bi])

def PredictBias(u,i,p,q,bu,bi,mu):
    ret = mu + bu[u] +bi[i]
    ret += sum([p[u][f]*q[i][f] for f in range(len(p[u]))])
    return ret

def LearningBiasLFM(train,F,n,alpha,lamdb,mu,k):
    [bu,bi,p,q] = InitBiasLFM(train,F)
    for step in range(n):
        for u,i,rui in train.items():
            pui = PredictBias(u,i,p,q,bu,bi,mu)
            eui = rui - pui
            bu[u] += alpha*(eui-lamdb*bu[u])
            bi[i] = alpha*(eui-lamdb*bi[i])
            for f in range(F):
                p[u][k] += alpha(q[i][k]*eui-lamdb*p[u][k])
                p[i][k] += alpha(p[u][k]*eui-lamdb*q[i][k])
        alpha *= 0.9
    return list([bu,bi,p,q])

#考虑邻域的偏置优化版
def LearningBiasLFM1(train_ui,F,n,alpha,lambd,mu,k):
    [bu,bi,p,q,y] = InitLFM(train_ui,F)
    z = {}
    for step in range(n):
        for u,items in train_ui.items():
            z[u] = p[u]
            ru = 1/math.sqrt(1.0*len(items))
            for i,rui in items.items():
                for f in range(F):
                    z[u][f] += y[i][f] *ru
                sum = [0 for i in range(F)]
                for i,rui in items.items():
                    pui = Predict(u,i,p,q)
                    eui = rui - pui
                    bu[u] += alpha*(eui-lambd*bu[u])
                    bi[i] += alpha*(eui-lambd*bi[i])
                    for f in range(F):
                        sum[k] += q[i][k] * eui *ru
                        p[u][k] += alpha*(q[i][k]*eui-lambd*p[u][k])
                        q[i][k] += alpha*((z[u][k]+p[u][k])*eui - lambd*q[i][k])
                for i,rui in items.items():
                    for f in range(F):
                        y[i][f] += alpha*(sum[f]-lambd*y[i][f])
                alpha *= 0.9
    return list([bu,bi,p,q])