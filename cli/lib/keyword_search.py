from typing import List
from lib.search_utils import Movie, load_movies, clean_text, tokenize_text


def is_token_in_title(query_tokens: list[str], title: str) -> bool:
    for token in query_tokens:
        if token in title:
            return True
    return False


def search_by_query(query: str, n_results: int) -> List[Movie]:
    result: List[Movie] = []

    movies = load_movies()
    query_tokens = tokenize_text(query)

    for movie in movies:
        title = clean_text(movie["title"])

        if is_token_in_title(query_tokens, title):
            result.append(movie)

        if len(result) == n_results:
            break
    result.sort(key=lambda v: v["id"])
    return result
