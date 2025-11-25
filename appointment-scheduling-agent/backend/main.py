
from fastapi import FastAPI, HTTPException
from .api import chat as chat_router
from .api import calendly_integration
from .models import schemas
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Appointment Scheduling Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router.router, prefix="/api")

@app.get("/api/calendly/availability")
def availability(date: str, appointment_type: str = "consultation"):
    try:
        return calendly_integration.get_availability(date, appointment_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/calendly/book")
def book(payload: dict):
    resp = calendly_integration.book_appointment(payload)
    if 'error' in resp:
        raise HTTPException(status_code=400, detail=resp['error'])
    return resp

if __name__ == '__main__':
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
