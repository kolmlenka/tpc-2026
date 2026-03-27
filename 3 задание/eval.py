import os
from collections import defaultdict
from parser import load_nerel_data
from model import NERModel


def evaluate(model: NERModel, texts, gold_entities):
    preds = model.predict_docs(texts)
    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)
    types = set()

    for pred_set, gold_list in zip(preds, gold_entities):
        gold_set = set(gold_list)

        for p in pred_set:
            if p in gold_set:
                tp[p[2]] += 1
            else:
                fp[p[2]] += 1
            types.add(p[2])

        for g in gold_set:
            if g not in pred_set:
                fn[g[2]] += 1
            types.add(g[2])

    f1s = []
    for t in types:
        t_tp = tp[t]
        t_fp = fp[t]
        t_fn = fn[t]

        prec = t_tp / (t_tp + t_fp) if (t_tp + t_fp) > 0 else 0.0
        rec  = t_tp / (t_tp + t_fn) if (t_tp + t_fn) > 0 else 0.0
        f1   = (2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0

        f1s.append(f1)

    return sum(f1s) / len(f1s) if f1s else 0.0


# model_path = os.path.join("models", "model.pkl.gz")

model = NERModel.load("models/model.pkl.gz")

texts, golds = load_nerel_data("NEREL/test")

mean_f1 = evaluate(model, texts, golds)

print("средний F1: " + str(mean_f1))
