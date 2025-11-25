
from typing import Dict, Any
from ..rag.faq_rag import FAQRAG
from ..api import calendly_integration

class SchedulingAgent:
    def __init__(self):
        self.rag = FAQRAG()

    def handle(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # very simple rule-based routing:
        lower = message.lower()
        if any(k in lower for k in ['book', 'appointment', 'see the doctor', 'schedule']):
            # start booking flow
            return {"type":"booking_start", "text":"Sure — what is the reason for your visit and which appointment type would you prefer (consultation/followup/physical/specialist)?"}
        if any(k in lower for k in ['where', 'hours', 'insurance', 'what should i bring', 'parking', 'cancel']):
            faq_answer = self.rag.answer(message)
            return {"type":"faq", "text": faq_answer}
        # fallback - small-chitchat
        return {"type":"fallback", "text":"I can help with scheduling appointments or answer clinic FAQs. Would you like to book or ask about clinic info?"}
