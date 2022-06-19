import ast
import sys, os
from os import times
from dotenv import load_dotenv
from time import time
from numpy import float128
from db.DBCon import DBCon

load_dotenv()

class ActivityUser:
    def __init__(self, activityId: str, userId: str, eScore:float, ) -> None:
        self.activityId = activityId
        self.userId = userId
        self.eScore = eScore

    def ActivityUserToDict(self) -> dict:
        return {
            'activityId': self.activityId,
            'userId': self.userId,
            'eScore': self.eScore
        }

    def ActivityUserToString(self) -> str:
        return str(self.ActivityUserToDict())

    @staticmethod
    def ActivityUserFromDict(activityUserDict: dict) -> None:
        return ActivityUser(
            activityUserDict['activityId'],
            activityUserDict['userId'],
            activityUserDict['eScore']
        )
    
    @staticmethod
    def ActivityUserFromString(activityUserStr: str) -> None:
        return ActivityUser.ActivityUserFromDict(ast.literal_eval(activityUserStr))


class ActivityUserStore:
    def __init__(self) -> None:
        self.db = DBCon (os.environ['DB_ACTIVITY_USER_LOC'])

    def putActivityUser(self, activityUser: ActivityUser) -> str:
        #get activity string
        activityUserStr = activityUser.ActivityUserToString()
        #generate random key
        key = str(time())
        #put key and activity string in db
        self.db.put(key, activityUserStr)
        return key

    def getActivityUser(self, key: str) -> ActivityUser:
        activityUserStr = self.db.get(key)
        return ActivityUser.ActivityUserFromString(activityUserStr)

    def getAllActivityUsers(self) -> list:
        activityUsers = []
        it = self.db.iteritems()
        it.seek_to_first()
        #check if there are any items in the db
        if it is not None:
            for key, value in it:
                value = value.decode('utf-8')
                #create activity object from string
                activityUser = ActivityUser.ActivityUserFromString(value)
                #add activity object to list
                activityUsers.append(activityUser)
        return activityUsers

    def getActivityUsersByActivityId(self, activityId: str) -> list:
        activityUsers = []
        it = self.db.iteritems()
        it.seek_to_first()
        #check if there are any items in the db
        if it is not None:
            for key, value in it:
                value = value.decode('utf-8')
                #create activity object from string
                activityUser = ActivityUser.ActivityUserFromString(value)
                #check if activityId matches
                if activityUser.activityId == activityId:
                    #add activity object to list
                    activityUsers.append(activityUser)
        return activityUsers

    def getActivityUsersByActivityId(self, activityUserList, activityId: str) -> list:
        activityUsers = []
        for activityUser in activityUserList:
            if activityUser.activityId == activityId:
                activityUsers.append(activityUser)
        return activityUsers



