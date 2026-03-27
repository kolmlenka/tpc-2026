import json
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from b3 import b3_precision_recall_f1

with open('dev-dataset-task2025-04.json') as f:
    raw = json.load(f)

texts = [item[0] for item in raw]
true_labels = [item[1] for item in raw]

with open("tfidf.pkl", "rb") as f:
    vectorizer = pickle.load(f)

X = vectorizer.transform(texts)

threshold = 0.35

pred_labels = []
clusters = []

for i in range(X.shape[0]):
    v = X[i]

    best_cluster = None
    best_sim = 0

    for cid, centroid in enumerate(clusters):
        sim = cosine_similarity(v, centroid)[0][0]
        if sim > best_sim:
            best_sim = sim
            best_cluster = cid

    if best_sim < threshold or best_cluster is None:
        clusters.append(v)
        pred_labels.append(len(clusters) - 1)
    else:
        pred_labels.append(best_cluster)

P, R, F1 = b3_precision_recall_f1(true_labels, pred_labels)

print("B3 precision:", P)
print("B3 recall:   ", R)
print("B3 F1:       ", F1)
