from operator import itemgetter

def addToMat(a,b,c,d):
    pass

def addToVec(a,b,c,):
    pass

def UserSimilarity(records):
    item_users,ave_vote,activity = {},{},{}
    for r in records:
        addToMat(item_users,r.item,r.user,r.value)
        addToVec(ave_vote,r.user,r.value)
        addToVec(activity,r.user,1)
    ave_vote = {x:y/activity[x] for x,y in ave_vote.items()}
    nu,W = {},{}
    for i,ri in item_users.items():
        for u,rui in ri.items():
            addToVec(nu,u,(rui-ave_vote[u]*(rui-ave_vote[u])))
            for v,rvi in ri.items():
                if u == v:
                    continue
                addToMat(W,u,v,(rui-ave_vote[u])*(rvi-ave_vote[v]))
    for u in W:
        W[u] = {x:y/math.sqrt(nu[x]*nu[u]) for x,y in W[u].items()}
    return W

def PredictAll(records,test,ave_vote,W,K):
    user_items = {}
    for r in records:
        addToMat(user_items,r.user,r.item,r.value)
    for r in test:
        r.predict,norm = 0,0
        for v,wuv in sorted(W[r.user].items(),key=itemgetter(1),reverse=True)[:K]:
            if r.item in user_items[v]:
                rvi = user_items[v][r.item]
                r.predict += wuv*(rvi-ave_vote[v])
                norm += abs(wuv)
                if norm > 0:
                    r.predict /= norm
                r.predict += ave_vote[r.user]
    return user_items