import math
import random
from operator import itemgetter

#分数据
def SplitData(records,train,test):
    for user,item,tag in records:
        if random.randint(1,10) == 1:
            test.append([user,item,tag])
        else:
            train.append([user,item,tag])
    return [train,test]

#计算标签流行度
def TagPopularity(records):
    tagfreq = {}
    for user,item,tag in records:
        if tag not in tagfreq:
            tagfreq[tag] = 1
        else:
            tagfreq[tag] += 1
    return tagfreq

#计算标签下的两个物品的余弦相似度
def ConsineSim(item_tags,i,j):
    ret = 0
    for b,wib in item_tags[i].items():
        if b in item_tags[j]:
            ret += wib*item_tags[j][b]
    ni,nj = 0,0
    for b ,w in item_tags[i].items():
        ni += w * w
    for b,w in item_tags[j].items():
        nj += w * w
    if ret == 0:
        return 0
    return ret/math.sqrt(ni*nj)

#多样性
def Diversity(item_tags,recommend_items):
    ret,n = 0,0
    for i in recommend_items.keys():
        for j in recommend_items.keys():
            if i == j:
                continue
            ret += ConsineSim(item_tags,i,j)
            n += 1
    return ret/(n*1.0)

def addValueToMat(a,b,c,d):
    pass

#初始化数据集
def InitStat(records,user_items):
    users_tags,tag_items,user_items = {},{},{}
    for user,item,tag in records.items():
        addValueToMat(users_tags,user,tag,1)
        addValueToMat(tag_items,tag,item,1)
        addValueToMat(user_items,user,item,1)

#用户个性化推荐
def Recommend(user,user_items,user_tags,tag_items):
    recommend_items = {}
    tagged_items = user_items[user]
    for tag,wut in user_tags[user].items():
        for item,wti in tag_items[tag].items():
            if item in tagged_items:
                continue
            if item not in recommend_items:
                recommend_items[item] = wut * wti
            else:
                recommend_items[item] += wut*wti
    return recommend_items

#推荐用户标签
def RecommendHybridPopularTags(user,item,user_tags,item_tags,alpha,N,ret):
    max_user_tag_weight = max(user_tags[user].values())
    for tag,weight in user_tags[user].items():
        ret[tag] = (1-alpha) * weight / max_user_tag_weight
    max_item_tag_weight = max(item_tags[item].values())
    for tag,weight in item_tags[item].items():
        if tag not in ret:
            ret[tag] = alpha * weight / max_item_tag_weight
        else:
            ret[tag] += alpha * weight / max_item_tag_weight
    return sorted(ret[user].items(),key=itemgetter(1),reverse=True)[:N]