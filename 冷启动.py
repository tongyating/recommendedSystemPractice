import math

def addToMat(a,b,c,d,e):
    pass

def addToVec(a,b,c):
    pass

#冷启动时计算物品的相似度
def CalculateSimilarity(entity_items):
    w ,ni ={},{}
    for e,items in entity_items.items():
        for i,wie in items.items():
            addToVec(ni,i,wie*wie)
            for j,wje in items.items():
                addToMat(w,i,j,wie,wje)
    for i,relate_items in w.items():
        relate_items = {x:y/math.sqrt(ni[i]*ni[x]) for x,y in relate_items.items()}






