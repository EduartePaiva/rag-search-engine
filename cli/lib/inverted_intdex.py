from lib.search_utils import load_movies, Movie, tokenize_text, PROJECT_ROOT
import pickle
import os
from collections import defaultdict


class InvertedIndex:
    def __init__(self) -> None:
        self.index: defaultdict[str, set[int]] = defaultdict(set)
        self.docmap: dict[int, Movie] = {}
        self.cache_path = PROJECT_ROOT / "cache"
        self.index_path = self.cache_path / "index.pkl"
        self.docmap_path = self.cache_path / "docmap.pkl"

    def __add_document(self, doc_id: int, text: str):
        text_tokens = tokenize_text(text)

        for token in text_tokens:
            self.index[token].add(doc_id)

    def get_documents(self, term: str):
        if len(self.docmap) == 0 or len(self.index) == 0:
            self.load()

        return sorted(list(self.index[term]))

    def build(self):
        print("building movies")
        movies = load_movies()

        for m in movies:
            self.docmap[m["id"]] = m
            self.__add_document(m["id"], f"{m['title']} {m['description']}")

    def load(self):
        with open(self.index_path, "rb") as f:
            self.index = pickle.load(f)

        with open(self.docmap_path, "rb") as f:
            self.docmap = pickle.load(f)

    def save(self):
        print("saving inverted index")
        os.makedirs(self.cache_path, exist_ok=True)

        with open(self.index_path, "wb") as f:
            pickle.dump(self.index, f)

        with open(self.docmap_path, "wb") as f:
            pickle.dump(self.docmap, f)
