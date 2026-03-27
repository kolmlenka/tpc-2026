from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


class Solution:
    def __init__(self):
        self.clusters = []
        self.labels = []
        self.next_label = 1
        with open("tfidf.pkl", "rb") as f:
            self.vectorizer = pickle.load(f)


    def predict(self, text: str) -> str:

        vec = self.vectorizer.transform([text]).toarray()[0]

        if len(self.clusters) == 0:
            self.clusters.append(vec)
            self.labels.append(self.next_label)
            self.next_label += 1
            return str(self.labels[-1])

        best_sim = -1
        best_idx = -1

        for idx, c in enumerate(self.clusters):
            sim = cosine_similarity([vec], [c])[0][0]
            if sim > best_sim:
                best_sim = sim
                best_idx = idx

        if best_sim > 0.4:
            self.clusters[best_idx] = (self.clusters[best_idx] + vec) / 2
            return str(self.labels[best_idx])
        else:
            self.clusters.append(vec)
            self.labels.append(self.next_label)
            self.next_label += 1
            return str(self.labels[-1])