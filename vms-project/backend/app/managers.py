# app/managers.py
import asyncio
import cv2
import time
from typing import Dict, List
from .models import StreamSchema, ResultSchema
from .motion_detector import MotionDetector

class ModelRegistry:
    def __init__(self):
        self.models = {}

    def register(self, name, model):
        self.models[name] = model

    def predict(self, name, frame):
        if name not in self.models:
            return {"error": f"Model {name} not found"}
        return self.models[name].predict(frame)

# global registry
model_registry = ModelRegistry()
model_registry.register("motion_detector", MotionDetector())

class StreamManager:
    def __init__(self):
        self.streams: Dict[str, StreamSchema] = {}
        self.results: Dict[str, List[ResultSchema]] = {}
        self.websockets: List = []

    async def run_stream(self, stream: StreamSchema):
        cap = cv2.VideoCapture(stream.source)
        if not cap.isOpened():
            print(f"❌ Could not open stream {stream.source}")
            stream.status = "error"
            return

        stream.status = "running"
        while stream.status == "running":
            ret, frame = cap.read()
            if not ret:
                break

            for model_name in stream.models:
                output = model_registry.predict(model_name, frame)
                result = ResultSchema(
                    stream_id=stream.id,
                    model=model_name,
                    output=output,
                    timestamp=time.time()
                )
                self.results.setdefault(stream.id, []).append(result)

                # send alert via websocket
                if output.get("alert"):
                    await self.broadcast({
                        "type": "alert",
                        "stream_id": stream.id,
                        "alert": output
                    })

            await asyncio.sleep(0.1)  # ~10 fps

        cap.release()
        stream.status = "stopped"

    async def stop_stream(self, stream_id: str):
        if stream_id in self.streams:
            self.streams[stream_id].status = "stopped"

    async def register(self, ws):
        self.websockets.append(ws)

    async def unregister(self, ws):
        if ws in self.websockets:
            self.websockets.remove(ws)

    async def broadcast(self, message: dict):
        to_remove = []
        for ws in self.websockets:
            try:
                await ws.send_json(message)
            except Exception:
                to_remove.append(ws)
        for ws in to_remove:
            await self.unregister(ws)

# global instance
stream_manager = StreamManager()