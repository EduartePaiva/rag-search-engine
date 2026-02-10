from lib.search_utils import load_movies, Movie, tokenize_text, PROJECT_ROOT
import pickle
import os


class InvertedIndex:
    index: dict[str, set[int]] = {}
    docmap: dict[int, Movie] = {}

    def __add_document(self, doc_id: int, text: str):
        text_tokens = tokenize_text(text)

        for token in text_tokens:
            index_tk = self.index.get(token, set())
            index_tk.add(doc_id)
            self.index[token] = index_tk

    def get_documents(self, term: str):
        term = tokenize_text(term)[0]

        return sorted(list(self.index[term]))

    def build(self):
        print("building movies")
        movies = load_movies()

        for i, m in enumerate(movies, 1):
            self.docmap[i] = m
            self.__add_document(i, f"{m['title']} {m['description']}")

    def save(self):
        print("saving inverted index")
        os.makedirs(PROJECT_ROOT / "cache", exist_ok=True)

        with open(
            PROJECT_ROOT / "cache" / "index.pkl",
            "wb",
        ) as docmap_file:
            pickle.dump(self.index, docmap_file)

        with open(
            PROJECT_ROOT / "cache" / "docmap.pkl",
            "wb",
        ) as docmap_file:
            pickle.dump(self.docmap, docmap_file)
