#innitiate the connection to RocksDB
import rocksdb
import sys
import os
import time
import json
import datetime
import logging
import logging.handlers
import logging.config

#create rocksdb crud object

class DBCon:
    def __init__(self,  db_path):
        opts = rocksdb.Options()
        opts.create_if_missing = True
        opts.max_open_files = 300000
        opts.write_buffer_size = 67108864
        opts.max_write_buffer_number = 3
        opts.target_file_size_base = 67108864
        opts.table_factory = rocksdb.BlockBasedTableFactory(
        filter_policy=rocksdb.BloomFilterPolicy(10),
        block_cache=rocksdb.LRUCache(2 * (1024 ** 3)),
        block_cache_compressed=rocksdb.LRUCache(500 * (1024 ** 2)))
        self.db = rocksdb.DB(db_path, opts)
        

    def get(self, key):
        #convert key to bytes
        key = key.encode('utf-8')
        #get value from db as bytes
        value = self.db.get(key)
        #check if value is not None
        if value is not None:
            #convert value to string
            value = value.decode('utf-8')
            return value
        else:
            return None

    def put(self, key, value):
        #convert key to bytes
        key = key.encode('utf-8')
        #convert string value to bytes
        value = value.encode('utf-8')
        #put key and value in db as bytes
        self.db.put(key, value)
    
    def delete(self, key):
        #convert key to bytes
        key = key.encode('utf-8')
        #delete key from db
        self.db.delete(key)

    def close(self):
        self.db.close()
    
    def get_multiple(self, keys):
        return self.db.multi_get(keys)
    
    def get_number_of_entries(self):
        it = self.db.iteritems()
        count = 0
        for key, value in it:
            count += 1
        return count

    def iteritems(self):
        return self.db.iteritems()

    def get_keys(self):
        return self.db.keys()

    def get_values(self):
        return self.db.values()
    
    def get_stats(self):
        return self.db.stats()

    def get_property(self, property):
        return self.db.property(property)

    def get_approximate_size(self, start, end):
        return self.db.approximate_size(start, end)

    def get_property_int(self, property):
        return self.db.property_int(property)

    def get_property_string(self, property):
        return self.db.property_string(property)
    
    def get_property_bool(self, property):
        return self.db.property_bool(property)

    

    