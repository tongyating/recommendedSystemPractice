#推荐模块的大体工作流程
def RecommendationCore(features,related_table):
    ret = {}
    for fid,fweight in features.items():
        for item,sim in related_table[fid].items():
            ret[item].wight += sim * fweight
            ret[item].reason[fid] = sim * fweight
    return ret

def sortByWeight(data):
    pass

#根据推荐理由增加推荐结果的多样性
def ReasonDiversity(recommendations):
    reasons = set()
    for i in recommendations:
        if i.reson in reasons:
            i.weight /= 2
        reasons.add(i.reson)
    recommendations = sortByWeight(recommendations)
