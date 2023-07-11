from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class CameraEvent(BaseModel):
    area: Optional[int] = None
    box:  Optional[List[int]] = []
    camera: str
    end_time: Optional[int] = None
    false_positive: Optional[str] = None
    has_clip: bool
    has_snapshot: bool
    id: str
    label: str
    plus_id: Optional[str] = None
    ratio: Optional[str] = None
    region: Optional[List[int]] = []
    retain_indefinitely: bool
    start_time: int
    sub_label: Optional[str] = None
    thumbnail: Optional[str]
    top_score: float
    zones: List[str] = []

class CameraEventQueryParams(BaseModel):
    before:	Optional[int]	#Epoch time
    after:	Optional[int]	#Epoch time
    cameras:	Optional[str]	#separated list of cameras
    labels:	Optional[str]	#separated list of labels
    zones:	Optional[str]	#separated list of zones
    limit:	Optional[int] = 20	#Limit the number of events returned
    has_snapshot:	Optional[int]	#Filter to events that have snapshots (0 or 1)
    has_clip:	Optional[int]	#Filter to events that have clips (0 or 1)
    include_thumbnails:	Optional[int]	#Include thumbnails in the response (0 or 1)
    in_progress:	Optional[int]	#Limit to events in progress (0 or 1)


class WsEventType(Enum):
    MOVEMENT = "movement"
    ADDMORE = "here"

class CameraNotification(BaseModel):
    id: str
    camera: str

class WebsocketEvent(BaseModel):
    type: WsEventType
    content: CameraNotification


