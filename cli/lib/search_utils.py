import json
from typing import TypedDict, List
from pathlib import Path
import string
from functools import lru_cache
from nltk.stem import PorterStemmer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "movies.json"
STOPWORDS_PATH = PROJECT_ROOT / "data" / "stopwords.txt"
STEAMER = PorterStemmer()


@lru_cache(maxsize=1)
def get_stopwords() -> frozenset[str]:
    with open(STOPWORDS_PATH, encoding="utf-8") as f:
        return frozenset(f.read().splitlines())


class Movie(TypedDict):
    id: int
    title: str
    description: str


def load_movies() -> List[Movie]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        json_movies = json.load(f)

    movies: List[Movie] = json_movies["movies"]

    return movies


def clean_text(text: str) -> str:
    # DO LOWERCASE
    text = text.lower()

    # CLEAN PUNCTUATION
    text = text.translate(str.maketrans("", "", string.punctuation))

    return text


def tokenize_text(text: str) -> list[str]:
    text = clean_text(text)
    tokens = set(text.split(" "))
    stopwords = get_stopwords()

    return [STEAMER.stem(t) for t in tokens if t not in stopwords]
