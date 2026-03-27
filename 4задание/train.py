import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

with open('dev-dataset-task2025-04.json') as f:
    raw_data = json.load(f)

# print(raw_data[:1])
texts = [item[0] for item in raw_data]

vectorizer = TfidfVectorizer()
vectorizer.fit(texts)

with open("tfidf.pkl", "wb") as f:
    pickle.dump(vectorizer, f)