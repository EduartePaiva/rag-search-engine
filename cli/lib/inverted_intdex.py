from lib.search_utils import (
    load_movies,
    Movie,
    tokenize_text,
    PROJECT_ROOT,
    clean_text,
    steam_words,
)
import pickle
import os
from collections import defaultdict, Counter
import math


class InvertedIndex:
    def __init__(self) -> None:
        self.index: defaultdict[str, set[int]] = defaultdict(set)
        self.docmap: dict[int, Movie] = {}
        self.cache_path = PROJECT_ROOT / "cache"
        self.index_path = self.cache_path / "index.pkl"
        self.docmap_path = self.cache_path / "docmap.pkl"
        self.term_frequencies_path = self.cache_path / "term_frequencies.pkl"
        self.term_frequencies: defaultdict[int, Counter[str]] = defaultdict(Counter)

    def get_idf(self, term: str) -> float:
        self.load()
        if not isinstance(term, str) or len(term.split()) > 1:
            raise ValueError("now allowed multiple term")
        term = tokenize_text(term)[0]
        total_doc_count = len(self.docmap)
        term_match_doc_count = len(self.index[term])

        idf = math.log((total_doc_count + 1) / (term_match_doc_count + 1))

        return idf

    def __add_document(self, doc_id: int, text: str):
        text_tokens = tokenize_text(text)

        for token in set(text_tokens):
            self.index[token].add(doc_id)

        self.term_frequencies[doc_id].update(steam_words(clean_text(text).split()))

    def get_documents(self, term: str):
        self.load()

        return sorted(list(self.index[term]))

    def get_tf(self, doc_id: int, term: str):
        self.load()
        if not isinstance(term, str) or len(term.split()) > 1:
            raise ValueError("now allowed multiple term")

        return self.term_frequencies[doc_id].get(term, 0)

    def build(self):
        print("building movies")
        movies = load_movies()

        for m in movies:
            self.docmap[m["id"]] = m
            self.__add_document(m["id"], f"{m['title']} {m['description']}")

    def load(self):
        if (
            len(self.docmap) > 0
            and len(self.index) > 0
            and len(self.term_frequencies) > 0
        ):
            return

        with open(self.index_path, "rb") as f:
            self.index = pickle.load(f)

        with open(self.docmap_path, "rb") as f:
            self.docmap = pickle.load(f)

        with open(self.term_frequencies_path, "rb") as f:
            self.term_frequencies = pickle.load(f)

    def save(self):
        print("saving inverted index")
        os.makedirs(self.cache_path, exist_ok=True)

        with open(self.index_path, "wb") as f:
            pickle.dump(self.index, f)

        with open(self.docmap_path, "wb") as f:
            pickle.dump(self.docmap, f)

        with open(self.term_frequencies_path, "wb") as f:
            pickle.dump(self.term_frequencies, f)
