import json
from solution import Solution
from b3 import b3_precision_recall_f1

with open('dev-dataset-task2025-04.json') as f:
    raw_data = json.load(f)[:100]

texts = [item[0] for item in raw_data]
true_labels = [item[1] for item in raw_data]

solver = Solution()

pred_labels = []
for text in texts:
    label = solver.predict(text)
    pred_labels.append(label)

P, R, F1 = b3_precision_recall_f1(true_labels, pred_labels)

print("B3 Precision:", P)
print("B3 Recall:   ", R)
print("B3 F1:       ", F1)