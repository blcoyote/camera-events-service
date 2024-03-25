import base64
import json
from typing import List, Optional
from loguru import logger
import pydantic
import requests
from models.event_model import CameraEvent, CameraEventQueryParams
from firebase_admin import credentials, messaging, initialize_app


def get_events(
    params: Optional[CameraEventQueryParams] = CameraEventQueryParams(),
) -> List[CameraEvent]:
    url = f"http://192.168.0.39:5000/api/events"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url, params=params.model_dump(), headers=headers)
        response.raise_for_status()
        adapter = pydantic.TypeAdapter(List[CameraEvent])
        data = adapter.validate_python(response.json())
        return data
    except Exception as e:
        logger.error(f"Error getting events from frigate: {e}")
        raise (e)


latest = get_events()[0]
creds_dict = json.loads(base64.b64decode("REMOVED BEFORE CHECKIN"))


def send_topic_push(event: CameraEvent):
    message = messaging.Message(
        topic="cameraevents",
        webpush=messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                title=f"Person set i kamera: {event.camera}",
                body=f"id: {event.id}",
            ),
            fcm_options=messaging.WebpushFCMOptions(
                link=f"https://ce.elcoyote.dk/eventnotification{event.id}",
            ),
            headers={"Urgency": "high"},
        ),
        android=messaging.AndroidConfig(
            notification=messaging.AndroidNotification(
                title=f"Person set i kamera: {event.camera}", body=f"id: {event.id}"
            ),
            ttl=36000,
            data={
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                "sound": "default",
                "status": "done",
                "path": f"/eventnotification",
                "id": event.id,
            },
        ),
    )
    messaging.send(message)


firebase_cred = credentials.Certificate(creds_dict)

firebase_app = initialize_app(firebase_cred)

send_topic_push(latest)
