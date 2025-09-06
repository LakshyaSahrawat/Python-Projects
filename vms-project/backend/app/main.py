# backend/app/main.py
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
import uuid

from app.models import StreamCreateRequest, StreamSchema, ResultSchema
from app.stream_manager import streams, results, run_stream
from app.broadcaster import Broadcaster

app = FastAPI(title="Video Management System")
broadcaster = Broadcaster()

@app.on_event("startup")
async def startup_event():
    samples = [
        {"source": "sample_videos/test1.mp4", "type": "file", "models": ["motion_detector"]},
        {"source": "sample_videos/test2.mp4", "type": "file", "models": ["motion_detector"]},
    ]
    for s in samples:
        stream_id = str(uuid.uuid4())
        stream_entry = {
            "id": stream_id,
            "source": s["source"],
            "type": s.get("type", "file"),
            "status": "starting",
            "fps": None,
            "models": s.get("models", ["motion_detector"]),
            "running": True
        }
        streams[stream_id] = stream_entry
        asyncio.create_task(run_stream(stream_entry, broadcaster=broadcaster))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/streams", response_model=StreamSchema)
async def create_stream(payload: StreamCreateRequest):
    stream_id = str(uuid.uuid4())
    stream_entry = {
        "id": stream_id,
        "source": payload.source,
        "type": payload.type,
        "status": "starting",
        "fps": None,
        "models": payload.models,
        "running": True
    }
    streams[stream_id] = stream_entry
    asyncio.create_task(run_stream(stream_entry, broadcaster=broadcaster))
    return StreamSchema(**stream_entry)

@app.get("/streams", response_model=List[StreamSchema])
async def list_streams():
    return [
        StreamSchema(
            id=s["id"],
            source=s["source"],
            type=s.get("type", "file"),
            status=s.get("status", "stopped"),
            fps=s.get("fps"),
            models=s.get("models", [])
        ) for s in streams.values()
    ]

@app.delete("/streams/{stream_id}")
async def stop_stream(stream_id: str):
    if stream_id not in streams:
        raise HTTPException(status_code=404, detail="Stream not found")
    streams[stream_id]["running"] = False
    return {"message": f"Stream {stream_id} stopped"}


@app.get("/results", response_model=List[ResultSchema])
async def list_results(limit: int = 20):
    last_results = list(results.values())[-limit:]
    return [
        ResultSchema(
            id=r["id"],
            stream_id=r["stream_id"],
            model=r["model"],
            output=r["output"],
            timestamp=r.get("timestamp", 0)
        ) for r in last_results
    ]


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await broadcaster.connect(ws)
    try:
        while True:
            await asyncio.sleep(5)
    finally:
        broadcaster.disconnect(ws)
