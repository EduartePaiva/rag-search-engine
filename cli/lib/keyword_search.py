from typing import List
from lib.search_utils import Movie, tokenize_text
from lib.inverted_intdex import InvertedIndex


def search_by_query(query: str, n_results: int) -> List[Movie]:
    result: List[Movie] = []
    idx = InvertedIndex()
    movie_ids: set[int] = set()
    query_tokens = tokenize_text(query)

    for query in query_tokens:
        ids = idx.get_documents(query)
        movie_ids.update(ids)

        if len(movie_ids) >= n_results:
            break

    for i, id in enumerate(sorted(movie_ids)):
        if i == n_results:
            break
        result.append(idx.docmap[id])

    return result
