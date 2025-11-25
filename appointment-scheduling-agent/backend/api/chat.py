
from fastapi import APIRouter
from pydantic import BaseModel
from ..agent.scheduling_agent import SchedulingAgent
from ..tools.availability_tool import suggest_slots
from ..tools.booking_tool import create_booking

router = APIRouter()
agent = SchedulingAgent()

class ChatRequest(BaseModel):
    message: str
    context: dict = {}

@router.post("/chat")
def chat(req: ChatRequest):
    res = agent.handle(req.message, req.context)
    # if agent asks to start booking, respond accordingly
    if res['type'] == 'booking_start':
        return {"reply": res['text'], "next": "collect_reason"}
    if res['type'] == 'faq':
        return {"reply": res['text'], "next": "faq"}
    if res['type'] == 'fallback':
        return {"reply": res['text'], "next": "fallback"}
    return {"reply": "Sorry, I didn't understand that."}
