
import json, os
from .embeddings import FAQRetriever

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'data', 'clinic_info.json')

class FAQRAG:
    def __init__(self):
        with open(DATA_PATH, 'r') as f:
            self.data = json.load(f)
        self.retriever = FAQRetriever([item['q'] + " " + item['a'] for item in self.data['faqs']])

    def answer(self, query: str) -> str:
        docs = self.retriever.retrieve(query, topk=2)
        # simple scoring: return best match if similarity > threshold
        if docs:
            return docs[0]['text']
        return "Sorry, I don't know the answer to that. Please contact the clinic at " + self.data.get('clinic_phone', '')
