import os
from dotenv import load_dotenv
from util import Singleton
import rocksdb3
from time import time
from util.helpers import convert_byte_string_to_json, convert_json_to_byte_string


load_dotenv()


class DatabaseService(metaclass=Singleton):
    def __init__(self, db_path='../db/test.db'):
        self.db = rocksdb3.open_default(db_path)
        print("Connected to Database Service")

    def tuple_to_json(i):
        return convert_byte_string_to_json(i[1])

    def get(self, key):
        value = self.db.get(key.encode('utf-8'))
        return convert_byte_string_to_json(value)

    def get_all(self):
        # get all keys from db
        values = list(self.db.get_iter())
        return list(map(self.tuple_to_json, values))

    def store_data(self, value, key=None):
        if(key == None):
            key = str(time())
        self.db.put(key.encode('utf-8'), convert_json_to_byte_string(value))

        return key


class ActivityClusterDatabaseService(DatabaseService):
    def __init__(self, ):
        super(DatabaseService, self).__init__(
            os.environ['DB_ACTIVITY_CLUSTER_LOC'])


class ClusterFeatureDatabaseService(DatabaseService):
    def __init__(self, ):
        super(DatabaseService, self).__init__(
            os.environ['DB_CLUSTER_FEATURE_LOC'])


class ActivityUserDatabaseService(DatabaseService):
    def __init__(self, ):
        super(DatabaseService, self).__init__(
            os.environ['DB_ACTIVITY_USER_LOC'])