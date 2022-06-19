from data_model.helper import *
import json


class FeatureResponse:
  def __init__(self, foreign_id, label,score):
    self.foreign_id = foreign_id
    self.label = label
    self.score=score
    
  def to_dict(self) -> dict:
        result: dict = {}
        result["foreign_id"] = from_str(self.foreign_id)
        result["label"] = from_str(self.label)
        result["score"] = from_float(self.score)
        return result
    
  def __str__(self):
     return json.dumps(self.to_dict());
