from typing import List, Optional
import pydantic
import requests
from lib.settings import get_settings
from models.event_model import CameraEvent, CameraEventQueryParams
from loguru import logger

def get_events(params: Optional[CameraEventQueryParams] = CameraEventQueryParams()) -> List[CameraEvent]: 
    url = f"{get_settings().frigate_baseurl}/api/events"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url, params=pydantic.parse_obj_as(dict, params), headers=headers)
        response.raise_for_status()
        out = pydantic.parse_obj_as(List[CameraEvent], response.json())
        return out
    except Exception as e:
        logger.error(f"Error getting events from frigate: {e}")
        raise(e)



def get_event(id: str) -> CameraEvent: 
    url = f"{get_settings().frigate_baseurl}/api/events/{id}"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    out = pydantic.parse_obj_as(CameraEvent, response.json())
    return out

def get_thumbnail(id: str) -> CameraEvent: 
    url = f"{get_settings().frigate_baseurl}/api/events/{id}/thumbnail.jpg"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, params=pydantic.parse_obj_as(dict), headers=headers)
    response.raise_for_status()
    out = pydantic.parse_obj_as(CameraEvent, response.json())
    return out

def get_snapshot(id: str) -> bytes:
    url = f"{get_settings().frigate_baseurl}/api/events/{id}/snapshot.jpg"
    response = requests.get(url).content
    return response

def get_latest(camera: str) -> bytes:
    url = f"{get_settings().frigate_baseurl}/api/{camera}/latest.jpg"
    response = requests.get(url).content
    return response


def get_clip(id: str) -> bytes:
    url = f"{get_settings().frigate_baseurl}/api/events/{id}/clip.mp4"
    response = requests.get(url).content
    return response