import gzip
import pickle
from typing import List, Tuple, Dict, Any, Set
from dataclasses import dataclass
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction import FeatureHasher
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from razdel import tokenize as razdel_tokenize


@dataclass
class Token:
    text: str
    start: int
    end: int
    

def tokenize_with_offsets(text: str):
    tokens = []
    for t in razdel_tokenize(text):
        tokens.append(Token(text=t.text, start=t.start, end=t.stop))
    return tokens
    

def token_features(tokens: List[Token], idx: int, window: int) -> Dict[str, Any]:
    feat = {}
    t = tokens[idx].text
    feat["word"] = t
    feat["lower"] = t.lower()
    feat["is_upper"] = str(t.isupper())
    feat["is_digit"] = str(t.isdigit())
    feat["len"] = str(min(len(t), 20))
    for L in (1,2,3):
        if len(t) >= L:
            feat[f"pref{L}"] = t[:L].lower()
            feat[f"suf{L}"] = t[-L:].lower()
    for d in range(1, window+1):
        if idx - d >= 0:
            td = tokens[idx-d].text
            feat[f"-{d}:word"] = td.lower()
        else:
            feat[f"-{d}:word"] = "BOS"
        if idx + d < len(tokens):
            td = tokens[idx+d].text
            feat[f"+{d}:word"] = td.lower()
        else:
            feat[f"+{d}:word"] = "EOS"
    feat["starts_with_upper"] = str(len(t)>0 and t[0].isupper())
    return feat


def spans_from_iob(tokens, labels):
    spans = set()
    cur_type = None
    cur_start = None

    for tok, lbl in zip(tokens, labels):
        if lbl.startswith("B-"):
            if cur_type is not None:
                spans.add((cur_start, prev_end, cur_type))

            cur_type = lbl[2:]
            cur_start = tok.start
            prev_end = tok.end

        elif lbl.startswith("I-") and cur_type == lbl[2:]:
            prev_end = tok.end

        else:
            if cur_type is not None:
                spans.add((cur_start, prev_end, cur_type))
            cur_type = None
            cur_start = None

    if cur_type is not None:
        spans.add((cur_start, prev_end, cur_type))

    return spans


class NERModel:

    def __init__(self, hash_size: int, window: int):
        self.hash_size = hash_size
        self.window = window
        self.hasher = FeatureHasher(n_features=self.hash_size, input_type='string')
        self.clf = None
        self.label_encoder = LabelEncoder()

    def featurize_docs(self, docs: List[dict]):
        X_items = []
        y = []
        token_lists = []
        for doc in docs:
            text = doc.get("text", "")
            tokens = tokenize_with_offsets(text)
            token_lists.append(tokens)
            labels = ["O"] * len(tokens)
            for e in doc.get("entities", []):
                s = e.get("start"); en = e.get("end"); typ = e.get("type")
                if s is None or en is None or typ is None:
                    continue
                idxs = [i for i,t in enumerate(tokens) if not (t.end <= s or t.start >= en)]
                if not idxs:
                    continue
                labels[idxs[0]] = f"B-{typ}"
                for ii in idxs[1:]:
                    labels[ii] = f"I-{typ}"
            for i in range(len(tokens)):
                feats = token_features(tokens, i, window=self.window)
                items = [f"{k}={v}" for k,v in feats.items()]
                X_items.append(items)
                y.append(labels[i])
        X = self.hasher.transform(X_items)
        return X, np.array(y), token_lists

    def fit(self, docs: List[dict], C: float, max_iter: int):
        X, y, _ = self.featurize_docs(docs)
        self.label_encoder.fit(y)
        y_enc = self.label_encoder.transform(y)
        clf = LogisticRegression(solver='saga', penalty='l2', C=C, max_iter=max_iter, n_jobs=1)
        clf.fit(X, y_enc)
        self.clf = clf

    def predict_docs(self, texts: List[str]):
        results = []
        for text in texts:
            tokens = tokenize_with_offsets(text)
            feats = []
            for i in range(len(tokens)):
                items = [f"{k}={v}" for k,v in token_features(tokens, i, window=self.window).items()]
                feats.append(items)
            if len(feats) == 0:
                results.append(set())
                continue
            X = self.hasher.transform(feats)
            if self.clf is None:
                results.append(set())
                continue
            y_pred_enc = self.clf.predict(X)
            y_pred = self.label_encoder.inverse_transform(y_pred_enc)
            spans = spans_from_iob(tokens, list(y_pred))
            results.append(spans)
        return results

    def save(self, path: str):
        state = {
            "hash_size": self.hash_size,
            "window": self.window,
            "label_encoder": self.label_encoder,
            "clf": self.clf
        }
        with gzip.open(path, "wb") as f:
            pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, path: str):
        with gzip.open(path, "rb") as f:
            state = pickle.load(f)
        obj = cls(hash_size=state.get("hash_size", 16384), window=state.get("window", 2))
        obj.label_encoder = state["label_encoder"]
        obj.clf = state["clf"]
        obj.hasher = FeatureHasher(n_features=obj.hash_size, input_type='string')
        return obj

