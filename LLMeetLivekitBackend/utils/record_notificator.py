
import json
from typing import List
from fastapi import WebSocket


class RecordNotificator:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def broadcast(self, message: dict):
        payload = json.dumps(message)
        for ws in self.active_connections:
            await ws.send_text(payload)

record_notificator = RecordNotificator()