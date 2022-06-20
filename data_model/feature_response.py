from data_model.helper import *
import json


class FeatureResponse:
  def __init__(self, activityId, feature,score,cluster=None):
    self.activityId = activityId
    self.score=score
    self.feature=feature
    self.cluster=cluster
    
  def to_dict(self) -> dict:
        result: dict = {}
        result["activityId"] = from_str(self.activityId)
        result["score"] = from_float(self.score)
        result["feature"] = from_str(self.feature)
        result["cluster"]= self.cluster
        return result
    
  def __str__(self):
     return json.dumps(self.to_dict());
