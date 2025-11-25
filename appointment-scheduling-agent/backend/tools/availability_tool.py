
from ..api.calendly_integration import get_availability

def suggest_slots(date: str, appointment_type: str):
    # return up to 5 available slots
    resp = get_availability(date, appointment_type)
    slots = [s for s in resp['available_slots'] if s['available']]
    return slots[:5]
