from __future__ import annotations

import argparse
from pathlib import Path

from app.store import VectorStore
from .loaders import load_and_chunk_directory


def ingest_directory_into_index(index_name: str, directory: Path, max_chars: int = 800) -> None:
    print(f"Ingesting directory '{directory}' into index '{index_name}'...")

    doc_chunks = load_and_chunk_directory(directory, max_chars=max_chars)
    if not doc_chunks:
        print("No valid .txt or .md files found. Nothing to ingest.")
        return

    store = VectorStore(index_name=index_name)

    for doc_id, chunks in doc_chunks.items():
        print(f"  - Ingesting doc_id='{doc_id}' with {len(chunks)} chunk(s)")
        store.add_texts(doc_id=doc_id, texts=chunks)

    print("Ingestion complete.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest .txt/.md files from a directory into a RAG index."
    )
    parser.add_argument(
        "--index",
        required=True,
        help="Name of the index (collection) to ingest into.",
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to directory with .txt/.md files.",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=800,
        help="Maximum characters per chunk (default: 800).",
    )

    args = parser.parse_args()

    directory = Path(args.path)
    ingest_directory_into_index(
        index_name=args.index,
        directory=directory,
        max_chars=args.max_chars,
    )


if __name__ == "__main__":
    main()
