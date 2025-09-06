# backend/app/models.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class StreamCreateRequest(BaseModel):
    source: str
    type: str = "file"
    models: List[str] = ["motion_detector"]

class StreamSchema(BaseModel):
    id: str
    source: str
    type: str
    status: str
    fps: Optional[float] = None
    models: List[str]

class ResultSchema(BaseModel):
    id: str
    stream_id: str
    model: str
    output: Dict[str, Any]
    timestamp: float
