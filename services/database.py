import os
from dotenv import load_dotenv
from util import *
import rocksdb3
import uuid
# from util.helpers import *


load_dotenv()


class DatabaseService(metaclass=Singleton):
    def __init__(self, db_path='../db/test.db'):
        self.db = rocksdb3.open_default(db_path)
        print("Connected to Database Service")

    def tuple_to_json(self, i):
        return convert_byte_string_to_json(i[1])

    def get(self, key):
        value = self.db.get(key.encode('utf-8'))
        if(value == None):
            return None
        return convert_byte_string_to_json(value)

    def get_all(self):
        # get all keys from db
        values = list(self.db.get_iter())
        if (values == None) or (len(values) == 0):
            return []
        return list(map(self.tuple_to_json, values))

    def put(self, value, key=None):
        if(key == None):
            key = str(uuid.uuid4())
        self.db.put(key.encode('utf-8'), convert_json_to_byte_string(value))

        return key

    def close(self):
        self.db.close()
        print("Closed Database Service")


class ActivityClusterDatabaseService(DatabaseService):
    def __init__(self):
        super(ActivityClusterDatabaseService, self).__init__(
            db_path=os.environ['DB_ACTIVITY_CLUSTER_LOC'])

    def getActivitiesByCluster(self, cluster: int):
        return list(map((lambda x: x['activityId']), list(filter(lambda x: x['cluster'] == cluster, self.get_all()))))

    def getActivityCluster(self, activityId):
        return list(filter(lambda x: x['activityId'] == activityId, self.get_all()))[0]['cluster']


class ClusterFeatureDatabaseService(DatabaseService):
    def __init__(self, ):
        super(ClusterFeatureDatabaseService, self).__init__(
            db_path=os.environ['DB_CLUSTER_FEATURE_LOC'])

    def getFeaturesByClusterId(self, cluster: int):
        return list(filter(lambda x: x['cluster'] == cluster, self.get_all()))

    def getClusterIdForFeature(self, cfs, feature: str):
        return list(filter(lambda x: x['feature'] == feature, cfs))[0]['cluster']


class ActivityUserDatabaseService(DatabaseService):
    def __init__(self):
        super(ActivityUserDatabaseService, self).__init__(
            db_path=os.environ['DB_ACTIVITY_USER_LOC'])

    def putOrUpdate(self, value, key=None):
        if(key == None):
            key = value['activityId'] + '_' + value['userId']

        old_value = self.get(key)
        if(old_value == None):
            self.put(value, key)
        else:
            old_value['score'] += value['score']
            self.put(old_value, key)

        self.db.put(key.encode('utf-8'), convert_json_to_byte_string(value))

        return key


class RewardsDatabaseService(DatabaseService):
    def __init__(self, ):
        super(ClusterFeatureDatabaseService, self).__init__(
            db_path=os.environ['DB_REWARDS_LOC'])
