
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

class FAQRetriever:
    def __init__(self, documents):
        self.documents = documents
        self.vectorizer = TfidfVectorizer(stop_words='english').fit(documents)
        self.doc_vectors = self.vectorizer.transform(documents)

    def retrieve(self, query, topk=3):
        qv = self.vectorizer.transform([query])
        sims = linear_kernel(qv, self.doc_vectors).flatten()
        idx = sims.argsort()[::-1][:topk]
        results = []
        for i in idx:
            results.append({"text": self.documents[i], "score": float(sims[i])})
        return results
