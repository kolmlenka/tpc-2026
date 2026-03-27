import os
import json
from typing import List
from parser import load_nerel_data
from model import NERModel


def build_docs_from_parser(texts: List[str], entities_list: List[List[tuple]]):
    docs = []
    for text, ents in zip(texts, entities_list):
        norm = []
        for (s, e, t) in ents:
            norm.append({"start": int(s), "end": int(e), "type": t})
        docs.append({"text": text, "entities": norm})
    return docs


train_texts, train_entities = load_nerel_data("NEREL/train")
train_docs = build_docs_from_parser(train_texts, train_entities)

model = NERModel(hash_size=16384, window=2)

print("Training")
model.fit(train_docs, C=1.0, max_iter=300)

os.makedirs("models", exist_ok=True)
out_path = os.path.join("models", "model.pkl.gz")

model.save(out_path)

print("Training complete")
