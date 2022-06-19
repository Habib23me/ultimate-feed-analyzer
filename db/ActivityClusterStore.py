#create Store object for Activities
import ast
import sys, os
from os import times
from dotenv import load_dotenv
from time import time
from numpy import float128
from db.DBCon import DBCon

load_dotenv()

class ActivityCluster: 
    def __init__(self, activityId: str, feature: str, score: float, clusterId: int) -> None:
        self.activityId = activityId
        self.feature = feature
        self.score = score
        self.cluster = clusterId

    def ActivityClusterToDict(self) -> dict:
        return {
            'activityId': self.activityId,
            'feature': self.feature,
            'score': self.score,
            'cluster': self.cluster
        }
    

    def ActivityClusterToString(self) -> str:
        return str(self.ActivityClusterToDict())
    
    @staticmethod
    def ActivityClusterFromDict(activityClusterDict: dict) -> None:
        return ActivityCluster(
            activityClusterDict['activityId'],
            activityClusterDict['feature'],
            activityClusterDict['score'],
            activityClusterDict['cluster']
        )

    @staticmethod
    def ActivityClusterFromString(activityClusterStr: str) -> None:
        return ActivityCluster.ActivityClusterFromDict(ast.literal_eval(activityClusterStr))
        # needs checking

class ActivityClusterStore:
    def __init__(self) -> None:
        print (os.environ['DB_ACTIVITY_CLUSTER_LOC'])
        self.db = DBCon (os.environ['DB_ACTIVITY_CLUSTER_LOC'])

    def putActivityCluster(self, activityCluster: ActivityCluster) -> str:
        #get activity string
        activityClusterStr = activityCluster.ActivityClusterToString()
        #generate random key
        key = str(time())
        #put key and activity string in db
        self.db.put(key, activityClusterStr)
        return key

    def getActivityCluster(self, key: str) -> ActivityCluster:
        #get activity string from db
        activityClusterStr = self.db.get(key)
        #convert activity string to activity object
        activityCluster = ActivityCluster.ActivityClusterFromString(activityClusterStr)
        return activityCluster

    def getAllActivityClusters(self) -> list:
        #get all keys from db
        it = self.db.iteritems()
        it.seek_to_first()
        #check if values is not None
        if it is not None:
            #iterate through keys and values
            activityClusters = []
            for key, value in it:
                value = value.decode('utf-8')
                #convert value to activity object
                activityCluster = ActivityCluster.ActivityClusterFromString(value)
                #add activity to list
                activityClusters.append(activityCluster)
            return activityClusters

    def getActivitiesByCluster(self, cluster: int) -> list:
        #get all keys from db
        it = self.db.iteritems()
        it.seek_to_first()
        #check if values is not None
        if it is not None:
            #iterate through keys and values
            activities = []
            for key, value in it:
                value = value.decode('utf-8')
                # print (value)
                #convert value to activity object
                activity = ActivityCluster.ActivityClusterFromString(value)
                #add activity to list
                if activity.cluster == cluster:
                    activities.append(activity)
            return activities
    
#mock data
# activityCluster = ActivityCluster('id1', 'feature2', 3, 4, 5)
# activityClusterStore = ActivityClusterStore()
# key = activityClusterStore.putActivityCluster(activityCluster)
# print (key)
# activityCluster2 = activityClusterStore.getActivityCluster(key)
# print (activityCluster2.ActivityClusterToString())
# activityClusters = activityClusterStore.getAllActivityClusters()
# print (activityClusters)
# activities = activityClusterStore.getActivitiesByCluster(4)
# print (activities[0].ActivityClusterToString())

    