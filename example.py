
def GetUserGroup(data):
    pass

def AddToMat(a,b,c,d):
    pass

#平均值预测器级联融合
def Predict(train,test,alpha=0.1):
    total,count = {},{}
    for record in train:
        gu = GetUserGroup(record.user)
        gi = GetUserGroup(record.item)
        AddToMat(total,gu,gi,record.vote-record.predict)
        AddToMat(count,gu,gi,1)
    for record in test:
        gu = GetUserGroup(record.user)
        gi = GetUserGroup(record.item)
        average = total[gu][gi] / (1.0 * count[gu][gi] + alpha)
        record.predict += average



