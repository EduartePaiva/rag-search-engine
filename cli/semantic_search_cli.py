#!/usr/bin/env python3

import argparse

from lib.semantic_search import (
    verify_model,
    embed_text,
    verify_embeddings,
    embed_query_text,
    search,
    chunk_text,
)


def main():
    parser = argparse.ArgumentParser(description="Semantic Search CLI")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("verify", help="Verify the semantic search model")

    chunk_parser = subparsers.add_parser("chunk", help="chunk text for processing")
    chunk_parser.add_argument("text", type=str, help="text to chunk")
    chunk_parser.add_argument(
        "chunk_size", type=int, nargs="?", default=200, help="Chunk size limit"
    )

    subparsers.add_parser(
        "verify_embeddings", help="Veryfy the embeddings for the movies"
    )

    search_parser = subparsers.add_parser(
        "search", help="Do a semantic search in movies"
    )
    search_parser.add_argument("query", type=str, help="query to search")
    search_parser.add_argument(
        "limit", type=int, nargs="?", default=5, help="Search limit"
    )
    embedquery_parser = subparsers.add_parser(
        "embedquery", help="Embeds the provided query"
    )
    embedquery_parser.add_argument("query", type=str, help="query to embbed")

    embed_text_parser = subparsers.add_parser("embed_text", help="embed a text")
    embed_text_parser.add_argument("text", type=str, help="text to be embeded")

    args = parser.parse_args()

    match args.command:
        case "verify":
            verify_model()
        case "embed_text":
            embed_text(args.text)
        case "verify_embeddings":
            verify_embeddings()
        case "embedquery":
            embed_query_text(args.query)
        case "search":
            search(args.query, args.limit)
        case "chunk":
            chunks = chunk_text(args.text, args.chunk_size)
            for c in chunks:
                print(f"Chunking {len(c)} characters")
                print(c)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
