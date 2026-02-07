from typing import List
from lib.search_utils import Movie, load_movies, clean_text


def search_by_query(query: str, n_results: int) -> List[Movie]:
    result: List[Movie] = []

    movies = load_movies()
    query = clean_text(query)

    for movie in movies:
        if query in clean_text(movie["title"]):
            result.append(movie)
            if len(result) == n_results:
                break

    result.sort(key=lambda v: v["id"])
    return result
