# backend/app/broadcaster.py
import asyncio

class Broadcaster:
    def __init__(self):
        self.connections = set()

    async def connect(self, websocket):
        await websocket.accept()
        self.connections.add(websocket)

    def disconnect(self, websocket):
        self.connections.discard(websocket)

    async def broadcast(self, payload: dict):
        to_remove = set()
        for ws in self.connections:
            try:
                await ws.send_json(payload)
            except:
                to_remove.add(ws)
        self.connections.difference_update(to_remove)
