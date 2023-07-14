from functools import lru_cache
import json
import os
import base64
import firebase_admin
from firebase_admin import credentials, messaging
from loguru import logger

from models.event_model import CameraEvent

firebase_app = None
creds_dict = json.loads(base64.b64decode(os.getenv("UVICORN_FIREBASE_CREDENTIALS")))

firebase_cred = credentials.Certificate(creds_dict)
topic = "cameraevents"

@lru_cache()
def get_firebase_app():
    firebase_app = firebase_admin.initialize_app(firebase_cred)
    return firebase_app


def subscribe_topic(tokens): # tokens is a list of registration tokens
 response = messaging.subscribe_to_topic(tokens, topic)
 if response.failure_count > 0:
  logger.error(f'Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason, response.errors))}')
        
def unsubscribe_topic(tokens): # tokens is a list of registration tokens
 response = messaging.unsubscribe_from_topic(tokens, topic)
 if response.failure_count > 0:
    logger.error(f'Failed to subscribe to topic {topic} due to {list(map(lambda e: e.reason, response.errors))}')
        
def send_topic_push(event: CameraEvent):
    
    message = messaging.Message(
        notification=messaging.Notification(
        title=f'Person set i kamera: {event.camera}',
        body=f'id: {event.id}'
        ),
        topic=topic,
        data={
            "click_action": "FLUTTER_NOTIFICATION_CLICK",
            "sound": "default", 
            "status": "done",
            "path":f"/eventnotification",
            'id': event.id,
            },
    )

    messaging.send(message)


def send_token_push(title, body, tokens):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
        title=title,
        body=body
        ),
        tokens=tokens
    )
    messaging.send_multicast(message)