from fastapi import WebSocket
from functools import lru_cache

@lru_cache()
def get_connection_manager():
    return ConnectionManager()

class ConnectionManager:
    def __init__(self):

        #Change to a list of objects to keep usernames and possibly subscriptions
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)