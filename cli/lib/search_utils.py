import json
from typing import TypedDict, List
from pathlib import Path
import string


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "movies.json"


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
