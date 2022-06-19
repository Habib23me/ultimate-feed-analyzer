from datetime import datetime
from typing import List, Any
import json
from data_model.helper import *



class Activity:
    actor: str
    time: datetime
    foreign_id: str
    media: List[str]
    caption: str

    def __init__(self, actor: str, time: datetime, foreign_id: str, media: List[str], caption: str) -> None:
        self.actor = actor
        self.time = time
        self.foreign_id = foreign_id
        self.media = media
        self.caption = caption

    @staticmethod
    def from_dict(obj: Any) -> 'Activity':
        assert isinstance(obj, dict)
        actor = from_str(obj.get("actor"))
        time = from_datetime(obj.get("time"))
        foreign_id = from_str(obj.get("foreign_id"))
        media = from_list(from_str, obj.get("media"))
        caption = from_str(obj.get("caption"))
        return Activity(actor, time, foreign_id, media, caption)

    def to_dict(self) -> dict:
        result: dict = {}
        result["actor"] = from_str(self.actor)
        result["time"] = self.time.isoformat()
        result["foreign_id"] = from_str(self.foreign_id)
        result["media"] = from_list(from_str, self.media)
        result["caption"] = from_str(self.caption)
        return result


def activity_from_dict(s: Any) -> Activity:
    return Activity.from_dict(s)
    
def activity_from_str(s:Any)-> Activity:
    return activity_from_dict(json.loads(s))

def activity_to_dict(x: Activity) -> Any:
    return to_class(Activity, x)