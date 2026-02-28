from sentence_transformers import SentenceTransformer
from models.search_types import Movie
import numpy as np
from lib.search_utils import CACHE_DIR, load_movies, cosine_similarity
import os


class SemanticSearch:
    def __init__(self) -> None:
        # Load the model (downloads automatically the first time)
        model = SentenceTransformer("all-MiniLM-L6-v2")
        self.model = model
        self.embbedings: None | np.ndarray = None
        self.documents: None | list[Movie] = None
        self.document_map: dict[int, Movie] = {}
        self.embbedings_path = os.path.join(CACHE_DIR, "movie_embeddings.npy")

    def search(self, query: str, limit: int):
        if self.embbedings is None or self.documents is None:
            raise ValueError(
                "No embeddings loaded. Call `load_or_create_embeddings` first."
            )
        query_embbeding = self.generate_embedding(query)

        similarity: list[tuple[float, int]] = []

        for i in range(len(self.embbedings)):
            cosine = cosine_similarity(query_embbeding, self.embbedings[i])
            similarity.append((cosine, i))

        similarity.sort(reverse=True)
        similarity = similarity[: min(len(similarity), limit)]

        return [
            {
                "title": self.documents[idx]["title"],
                "description": self.documents[idx]["description"],
                "score": score,
            }
            for (score, idx) in similarity
        ]

    def generate_embedding(self, text: str) -> np.ndarray:
        if len(text.strip()) == 0:
            raise ValueError("text should not be empty")

        embeddings = self.model.encode([text])
        return embeddings[0]

    def load_or_create_embeddings(self, documents: list[Movie]):
        self.documents = documents
        for m in documents:
            self.document_map[m["id"]] = m

        if os.path.exists(self.embbedings_path):
            embbedings = np.load(self.embbedings_path)
            if len(embbedings) == len(documents):
                self.embbedings = embbedings
                return self.embbedings

        return self.build_embeddings(documents)

    def build_embeddings(self, documents: list[Movie]):
        self.documents = documents
        movie_strings = []
        for m in documents:
            self.document_map[m["id"]] = m
            movir_string = f"{m['title']}: {m['description']}"
            movie_strings.append(movir_string)

        encoded_movies = self.model.encode(movie_strings, show_progress_bar=True)

        self.embbedings = encoded_movies

        np.save(self.embbedings_path, encoded_movies)

        return encoded_movies


def search(query: str, limit=5):
    semantic_search = SemanticSearch()
    movies = load_movies()
    semantic_search.load_or_create_embeddings(movies)

    results = semantic_search.search(query, limit)

    for i, movie in enumerate(results, 1):
        print(
            f"{i}. {movie['title']} (score: {movie['score']:.4f}) \n   {movie['description'][:min(len(movie['description']), 80)]}..."
        )


def chunk_text(text: str, chunk_size: int):
    words = text.split()
    chunks: list[str] = []

    for i in range(0, len(words), chunk_size):
        chunk = words[i : min(len(words), i + chunk_size)]
        chunks.append(" ".join(chunk))

    return chunks


def embed_query_text(query: str):
    semantic_search = SemanticSearch()
    embedding = semantic_search.generate_embedding(query)

    print(f"Query: {query}")
    print(f"First 5 dimensions: {embedding[:5]}")
    print(f"Shape: {embedding.shape}")


def verify_embeddings():
    semantic_search = SemanticSearch()
    movies = load_movies()

    embeddings = semantic_search.load_or_create_embeddings(movies)

    print(f"Number of docs:   {len(movies)}")
    print(
        f"Embeddings shape: {embeddings.shape[0]} vectors in {embeddings.shape[1]} dimensions"
    )


def embed_text(text: str):
    semantic_search = SemanticSearch()
    embedding = semantic_search.generate_embedding(text)

    print(f"Text: {text}")
    print(f"First 3 dimensions: {embedding[:3]}")
    print(f"Dimensions: {embedding.shape[0]}")


def verify_model():
    semantic_search = SemanticSearch()

    print(f"Model loaded: {semantic_search.model}")
    print(f"Max sequence length: {semantic_search.model.max_seq_length}")
