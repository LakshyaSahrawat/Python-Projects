
from ..api.calendly_integration import book_appointment

def create_booking(appointment_type, date, start_time, patient, reason=None):
    payload = {
        "appointment_type": appointment_type,
        "date": date,
        "start_time": start_time,
        "end_time": None,
        "patient": patient,
        "reason": reason
    }
    return book_appointment(payload)
