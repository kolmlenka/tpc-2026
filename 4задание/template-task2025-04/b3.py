from collections import defaultdict

def b3_precision_recall_f1(true_labels, pred_labels):

    N = len(true_labels)

    true_clusters = defaultdict(set)
    pred_clusters = defaultdict(set)

    for i, t in enumerate(true_labels):
        true_clusters[t].add(i)

    for i, p in enumerate(pred_labels):
        pred_clusters[p].add(i)

    precision_sum = 0.0
    recall_sum = 0.0

    for i in range(N):
        t = true_labels[i]
        p = pred_labels[i]

        true_set = true_clusters[t]
        pred_set = pred_clusters[p]

        intersection_size = len(true_set & pred_set)

        precision_sum += intersection_size / len(pred_set)
        recall_sum += intersection_size / len(true_set)

    P = precision_sum / N
    R = recall_sum / N

    if P + R == 0:
        return P, R, 0.0

    F1 = 2 * P * R / (P + R)
    return P, R, F1
