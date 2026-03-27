from typing import List, Iterable, Set, Tuple
import os
from model import NERModel

# MODEL_PATH = os.path.join("models/model.pkl.gz")

class Solution:
    def __init__(self):
        self.model = None
        if os.path.exists("models/model.pkl.gz"):
            self.model = NERModel.load("models/model.pkl.gz")
        else:
            self.model = None

    def predict(self, texts: List[str]) -> Iterable[Set[Tuple[int, int, str]]]:
        if self.model is None:
            return [set() for _ in texts]
        return self.model.predict_docs(texts)

