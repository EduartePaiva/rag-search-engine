#!/usr/bin/env python3

import argparse
import json
from typing import TypedDict, List


class Movie(TypedDict):
    id: int
    title: str
    description: str


def search_by_keyword(query: str) -> List[Movie]:
    result: List[Movie] = []

    with open("./data/movies.json", "r", encoding="utf-8") as file:
        json_movies = json.load(file)

    movies: List[Movie] = json_movies["movies"]
    query = query.lower()

    for movie in movies:
        if movie["title"].lower().find(query):
            print(movie)
            result.append(movie)
            if len(result) == 5:
                break

    result.sort(key=lambda v: v["id"])
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            movies_found = search_by_keyword(args.query)
            print(movies_found)
            pass
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
