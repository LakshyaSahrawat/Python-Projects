
import json, uuid
from datetime import datetime, timedelta
from ..models.schemas import AvailabilityResponse, AvailabilitySlot, BookingResponse
from typing import List
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'data', 'doctor_schedule.json')
DATA_PATH = os.path.normpath(DATA_PATH)

def _load_schedule():
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

def _save_schedule(data):
    with open(DATA_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def get_availability(date: str, appointment_type: str) -> dict:
    data = _load_schedule()
    duration_min = data['event_types'].get(appointment_type, 30)
    # working hours - simple fixed slots 09:00 to 17:00
    start_hour = 9
    end_hour = 17
    slots = []
    current = datetime.fromisoformat(f"{date}T{start_hour:02d}:00")
    end_dt = datetime.fromisoformat(f"{date}T{end_hour:02d}:00")
    bookings = [b for b in data.get('bookings', []) if b['date'] == date]
    while current + timedelta(minutes=duration_min) <= end_dt:
        st = current.strftime('%H:%M')
        en = (current + timedelta(minutes=duration_min)).strftime('%H:%M')
        # check overlap with bookings
        occupied = False
        for b in bookings:
            if not (en <= b['start_time'] or st >= b['end_time']):
                occupied = True
                break
        slots.append({"start_time": st, "end_time": en, "available": not occupied})
        current += timedelta(minutes=duration_min)
    return {"date": date, "available_slots": slots}

def book_appointment(payload: dict) -> dict:
    data = _load_schedule()
    # simple conflict check
    for b in data.get('bookings', []):
        if b['date'] == payload['date'] and b['start_time'] == payload['start_time']:
            return {"error": "Slot already booked"}
    booking_id = "APPT-" + uuid.uuid4().hex[:8].upper()
    confirmation = uuid.uuid4().hex[:6].upper()
    new = {
        "date": payload['date'],
        "start_time": payload['start_time'],
        "end_time": payload.get('end_time'),
        "appointment_type": payload['appointment_type'],
        "patient": payload['patient'],
        "reason": payload.get('reason'),
        "booking_id": booking_id,
        "confirmation_code": confirmation
    }
    data.setdefault('bookings', []).append(new)
    _save_schedule(data)
    return {"booking_id": booking_id, "status": "confirmed", "confirmation_code": confirmation, "details": new}
