#!/usr/bin/env python3

import argparse
from lib.keyword_search import search_by_query
from lib.inverted_intdex import InvertedIndex


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.add_parser("build", help="Build and save inverted index")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            movies_found = search_by_query(args.query, 5)

            for i, m in enumerate(movies_found, 1):
                print(f"{i}. Movie {m['title']}")
            pass
        case "build":
            inverted_index = InvertedIndex()

            inverted_index.build()
            inverted_index.save()
            docs = inverted_index.get_documents("merida")

            print(f"First document for token 'merida' = {docs[0]}")

            pass

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
