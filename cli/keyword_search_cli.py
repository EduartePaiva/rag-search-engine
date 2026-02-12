#!/usr/bin/env python3

import argparse
from lib.keyword_search import search_by_query, tokenize_text
from lib.inverted_intdex import InvertedIndex


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.add_parser("build", help="Build and save inverted index")

    term_frequency = subparsers.add_parser("tf", help="Search a term frequency")
    term_frequency.add_argument("doc_id", type=int, help="document id to search")
    term_frequency.add_argument("term", type=str, help="term to search")

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
            pass

        case "tf":
            inverted_index = InvertedIndex()
            doc_id = args.doc_id
            term = tokenize_text(args.term)[0]

            print(inverted_index.get_tf(doc_id, term))
            pass

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
