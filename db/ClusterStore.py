from DBCon import DBCon
from Cluster import Cluster
from time import time
import util.DBLoc 
class ClusterStore:
    def __init__(self):
        self.db = DBCon(util.DBLoc.DB_CLUSTER_LOC)

    def putCluster(self, cluster: Cluster) -> str:
        #get cluster string
        clusterStr = cluster.stringify()
        #generate random key
        key = str(time())
        #put key and cluster string in db
        self.db.put(key, clusterStr)
        return key

    

    def getCluster(self, key: str) -> Cluster:
        #get cluster string from db
        clusterStr = self.db.get(key)
        #convert cluster string to cluster object
        cluster = Cluster.parse(clusterStr)
        return cluster

    def getClusters(self, keys) -> list:
        #get clusters from db
        clusters = self.db.get_multiple(keys)
        #convert clusters to cluster objects
        clusters = [Cluster.parse(cluster) for cluster in clusters]
        return clusters

    def getAllClusters(self) -> list:
        #get all keys from db
        it = self.db.iteritems()
        it.seek_to_first()
        #check if values is not None 
        if it is not None:
            #iterate through keys and values
            clusters = []
            for key, value in it:
                value = value.decode('utf-8')
                print (value)
                #convert value to cluster object
                cluster = Cluster.parse(value)
                #add cluster to list
                clusters.append(cluster)
            return clusters

    def getClusterByFeature(self, feature: str) -> list:
        #get all keys from db
        it = self.db.iteritems()
        it.seek_to_first()
        #check if values is not None
        if it is not None:
            #iterate through keys and values
            clusters = []
            for key, value in it:
                value = value.decode('utf-8')
                print (value)
                #convert value to cluster object
                cluster = Cluster.parse(value)
                #add cluster to list
                clusters.append(cluster)
            for cluster in clusters:
                if feature in cluster.getFeatures():
                    return cluster
        return None

#mock ClusterStore object
clusterStore = ClusterStore()
cluster = Cluster("cluster1", ["feature1", "feature2"])
key = clusterStore.putCluster(cluster)
print(key)
cluster = clusterStore.getCluster(key)
print(cluster.stringify())
clusters = clusterStore.getAllClusters()
print(clusters)
clusters = clusterStore.getClusterByFeature("feature1")
print(clusters)
clusters = clusterStore.getClusterByFeature("feature3")
print(clusters)