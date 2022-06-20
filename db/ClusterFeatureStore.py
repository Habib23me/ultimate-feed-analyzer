# import ast
# import sys, os
# from os import times
# from dotenv import load_dotenv
# from time import time
# from numpy import float128
# from db.DBCon import DBCon

# load_dotenv()

# class ClusterFeature:
#     def __init__(self, clusterId: int, feature: str) -> None:
#         self.clusterId = clusterId
#         self.feature = feature 

#     def ClusterFeatureToDict(self) -> dict:
#         return {
#             'clusterId': self.clusterId,
#             'feature': self.feature
#         }
    
#     def ClusterFeatureToString(self) -> str:
#         return str(self.ClusterFeatureToDict())

#     @staticmethod
#     def ClusterFeatureFromDict(clusterFeatureDict: dict) -> None:
#         return ClusterFeature(
#             clusterFeatureDict['clusterId'],
#             clusterFeatureDict['feature']
#         )
    
#     @staticmethod
#     def ClusterFeatureFromString(clusterFeatureStr: str) -> None:
#         return ClusterFeature.ClusterFeatureFromDict(ast.literal_eval(clusterFeatureStr))


# class ClusterFeatureStore:
#     def __init__(self) -> None:
#         print (os.environ['DB_CLUSTER_FEATURE_LOC'])
#         self.db = DBCon (os.environ['DB_CLUSTER_FEATURE_LOC'])
    
#     def putClusterFeature(self, clusterFeature: ClusterFeature) -> str:
#         #get activity string
#         clusterFeatureStr = clusterFeature.ClusterFeatureToString()
#         #generate random key
#         key = str(time())
#         #put key and activity string in db
#         self.db.put(key, clusterFeatureStr)
#         return key

#     def getClusterFeature(self, key: str) -> ClusterFeature:
#         clusterFeatureStr = self.db.get(key)
#         return ClusterFeature.ClusterFeatureFromString(clusterFeatureStr)

#     def getAllClusterFeatures(self) -> list:
        
#         it = self.db.iteritems()
#         it.seek_to_first()
#         if it is not None:
#             clusterFeatures = []
#         #check if there are any items in the db
#             for key, value in it:
#                 value = value.decode('utf-8')
#                 clusterFeature = ClusterFeature.ClusterFeatureFromString(value)
#                 clusterFeatures.append(clusterFeature)
#         return clusterFeatures

#     def getFeaturesByClusterId(self, clusterId: int) -> list:
#         clusterFeatures = []
#         it = self.db.iteritems()
#         it.seek_to_first()
#         #check if there are any items in the db
#         for key, value in it:
#             value = value.decode('utf-8')
#             clusterFeature = ClusterFeature.ClusterFeatureFromString(value)
#             if (clusterFeature.clusterId == clusterId):
#                 clusterFeatures.append(clusterFeature)
#         return clusterFeatures

#     def getClusterIdForFeature(self, cfs, feature: str) -> int:
#         clusterId = -1
#         type(cfs)
#         for cf in cfs:
#             if (cf.feature == feature):
#                 clusterId = cf.clusterId
#                 break
#         return clusterId

#     def close(self) -> None:
#         self.db.close()
# #mock data
# clusterFeatures = [
#    ClusterFeature(1, 'feature1'),
#    ClusterFeature(2, 'feature2'),
#    ClusterFeature(3, 'feature3'),
#    ClusterFeature(4, 'feature4'),
#    ClusterFeature(5, 'feature5'),
#    ClusterFeature(6, 'feature6'),
#    ClusterFeature(7, 'feature7'),
#    ClusterFeature(8, 'feature8'),
# ]
# clusterFeatureStore = ClusterFeatureStore()
# # keys = []
# # for clusterFeature in clusterFeatures:
# #     key = clusterFeatureStore.putClusterFeature(clusterFeature)
# #     print (key)
# #     keys.append(key)
# #     clusterFeature = clusterFeatureStore.getClusterFeature(key)
# #     print (clusterFeature.ClusterFeatureToString())

# # for clusterFeature in clusterFeatures:
# #     print(clusterFeatureStore.getClusterFeature(clusterFeature.ClusterFeatureToString()))

# # for clusterFeature in clusterFeatures:
# #     print(clusterFeatureStore.getFeaturesByClusterId(clusterFeature.clusterId))
# # print(clusterFeatureStore.getAllClusterFeatures())
# cfs = clusterFeatureStore.getFeaturesByClusterId(1)
# for cf in cfs:
#     print(cf.ClusterFeatureToString())
