import math

def addToDict(a,b,c):
    pass

def Recommend(uid,familiarity,similiarity,train):
    rank ={}
    interacted_items = train[uid]
    for fid,fw in familiarity[uid]:
        for item,pw in train[fid]:
            if item in interacted_items:
                continue
            addToDict(rank,item,fw*pw)
    for vid,sw in similiarity[uid]:
        for item,pw in train[vid]:
            if item in interacted_items:
                continue
            addToDict(rank,item,sw*pw)
    return rank

#好友推荐算法
def FriendSuggestion0(user,G,GT):
    suggestions = {}
    friends = G[user]
    for fid in G[user]:
        for ffid in GT[fid]:
            if ffid in friends:
                continue
            if ffid not in suggestions:
                suggestions[ffid] = 0
            suggestions[ffid] += 1
    suggestions = {x:y/math.sqrt(len(G[user])*len(G[x])) for x,y in suggestions}
    return suggestions

def FriendSuggestion1(user,G,GT):
    suggestions = {}
    friends = G[user]
    for fid in GT[user]:  #不同
        for ffid in GT[fid]:
            if ffid in friends:
                continue
            if ffid not in suggestions:
                suggestions[ffid] = 0
            suggestions[ffid] += 1
    suggestions = {x:y/math.sqrt(len(G[user])*len(G[x])) for x,y in suggestions}
    return suggestions
