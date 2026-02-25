#!/usr/bin/env python3

import argparse

from lib.semantic_search import (
    verify_model,
    embed_text,
    verify_embeddings,
    embed_query_text,
)


def main():
    parser = argparse.ArgumentParser(description="Semantic Search CLI")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("verify", help="Verify the semantic search model")

    subparsers.add_parser(
        "verify_embeddings", help="Veryfy the embeddings for the movies"
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
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
