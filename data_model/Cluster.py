class Cluster:
    def __init__(self, name, features):
        self.name = name
        self.features = features

    def getName(self):
        return self.name
    
    def getFeatures(self):
        return self.features

    def stringify(self):
        features = ",".join(item for item in self.features)
        cluster = self.name + "," + features
        return cluster

    def parse(clusterStr):
        cluster = clusterStr.split(",")
        name = cluster[0]
        features = cluster[1:]
        return Cluster(name, features)