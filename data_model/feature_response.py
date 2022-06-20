from data_model.helper import *
import json


class FeatureResponse:
  def __init__(self, activity_id, feature,score,cluster=None):
    self.activity_id = activity_id
    self.score=score
    self.feature=feature
    self.cluster=cluster
    
  def to_dict(self) -> dict:
        result: dict = {}
        result["activity_id"] = from_str(self.activity_id)
        result["score"] = from_float(self.score)
        result["feature"] = from_str(self.feature)
        result["cluster"]= from_int(self.cluster)
        return result
    
  def __str__(self):
     return json.dumps(self.to_dict());
