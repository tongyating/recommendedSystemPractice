from operator import itemgetter


class Cluster:
    def __init__(self, records):
        self.group = {}

    def GetGroup(selfself, i):
        return 0


class IdCluster(Cluster):
    def __init__(self, records):
        Cluster.__init__(self, records)

    def GetGroup(selfself, i):
        return i


class UserActivityCluster(Cluster):
    def __init__(self, records, basic):
        Cluster.__init__(self, records)
        activity = {}
        for r in records:
            if r.test != 0:
                continue
            basic.AddToDict(activity, r.user, 1)
        k = 0
        for user, n in sorted(activity.items(), key=itemgetter(1), reverse=False):
            c = int((k * 5) / (1.0 * len(activity)))
            self.group[user] = c
            k += 1

    def GetGroup(self, uid):
        if uid not in self.group:
            return -1
        else:
            return self.group[uid]


class ItemPopularityCluster(Cluster):
    def __init__(self, records, basic):
        Cluster.__init__(self, records)
        popularity = {}
        for r in records:
            if r.test != 0:
                continue
            basic.AddToDict(popularity, r.item, 1)
        k = 0
        for item, n in sorted(popularity.items(), key=itemgetter(1), reverse=False):
            c = int((k * 5) / (1.0 * len(popularity)))
            self.group[item] = c
            k += 1

    def GetGroup(self, item):
        if item not in self.group:
            return -1
        else:
            return self.group[item]


class UserVoteCluster(Cluster):
    def __init__(self, records, basic):
        Cluster.__init__(self, records)
        vote, count = {}, {}
        for r in records:
            if r.test != 0:
                continue
            basic.AddToDict(vote, r.user, r.vote)
            basic.AddToDict(count, r.user, 1)
        k = 0
        for user, v in vote.items():
            ave = v / (count[user] * 1.0)
            c = int(ave * 2)
            self.group[user] = c

    def GetGroup(self, uid):
        if uid not in self.group:
            return -1
        else:
            return self.group[uid]


class ItemVoteCluster(Cluster):
    def __init__(self, records, basic):
        Cluster.__init__(self, records)
        vote, count = {}, {}
        for r in records:
            if r.test != 0:
                continue
            basic.AddToDict(vote, r.user, r.vote)
            basic.AddToDict(count, r.user, 1)
        k = 0
        for item, v in vote.items():  # 不同
            ave = v / (count[item] * 1.0)  # 不同
            c = int(ave * 2)
            self.group[item] = c  # 不同

    def GetGroup(self, item):  # 不同
        if item not in self.group:  # 不同
            return -1
        else:
            return self.group[item]  # 不同


def PredictAll(records,user_cluster,item_cluster,basic):
    total, count = {},{}
    for r in records:
        if r.test != 0:
            continue
        gu = user_cluster.GetGroup(r.user)
        gi = item_cluster.GetGroup(r.item)
        basic.AddToMat(total,gu,gi,r.vote)
        basic.AddToMat(count,gu,gi,1)
    for r in records:
        gu = user_cluster.GetGroup(r.user)
        gi = item_cluster.GetGroup(r.item)
        average = total[gu][gi] / (1.0*count[gu][gi] + 1.0)
        r.predict = average
