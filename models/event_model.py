from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum


class DataModel(BaseModel):
    box: List[float] = []
    region: List[float] = []
    score: Optional[float] = None
    top_score: Optional[float] = None
    type: str


class CameraEvent(BaseModel):
    data: Optional[DataModel] = None
    camera: str
    end_time: Optional[float] = None
    false_positive: Optional[bool] = None
    has_clip: bool
    has_snapshot: bool
    id: str
    label: str
    plus_id: Optional[str] = None
    retain_indefinitely: bool
    start_time: float
    sub_label: Optional[str] = None
    thumbnail: Optional[str] = None
    zones: List[str] = []

class CameraEventQueryParams(BaseModel):
    before: Optional[int] = None  # Epoch time
    after: Optional[int] = None  # Epoch time
    cameras: Optional[str] = None  # separated list of cameras
    labels: Optional[str] = None  # separated list of labels
    zones: Optional[str] = None  # separated list of zones
    limit: Optional[int] = 20  # Limit the number of events returned
    has_snapshot: Optional[int] = None  # Filter to events that have snapshots (0 or 1)
    has_clip: Optional[int] = None  # Filter to events that have clips (0 or 1)
    include_thumbnails: Optional[int] = (
        None  # Include thumbnails in the response (0 or 1)
    )
    in_progress: Optional[int] = None  # Limit to events in progress (0 or 1)


class WsEventType(Enum):
    MOVEMENT = "movement"
    ADDMORE = "here"

class CameraNotification(BaseModel):
    id: str
    camera: str

class WebsocketEvent(BaseModel):
    type: WsEventType
    content: CameraNotification
