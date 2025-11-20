from __future__ import annotations

from pathlib import Path
from typing import List


def load_text_file(path: Path) -> str:
    """
    Load a .txt or .md file as a single string.
    """
    return path.read_text(encoding="utf-8")


def simple_chunk_text(text: str, max_chars: int = 800) -> List[str]:
    """
    Naive chunker: splits text into chunks of up to max_chars,
    trying to break on sentence / paragraph boundaries where possible.
    """
    text = text.strip()
    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        # If paragraph alone is longer than max_chars, hard-split it
        if len(para) > max_chars:
            # Flush current if it has content
            if current:
                chunks.append(current.strip())
                current = ""
            # Hard split long paragraph
            for i in range(0, len(para), max_chars):
                chunks.append(para[i : i + max_chars].strip())
            continue

        # If adding this paragraph exceeds max_chars, flush current
        if len(current) + len(para) + 2 > max_chars:  # +2 for spacing
            if current:
                chunks.append(current.strip())
            current = para
        else:
            if current:
                current += "\n\n" + para
            else:
                current = para

    if current:
        chunks.append(current.strip())

    return chunks


def load_and_chunk_directory(path: Path, max_chars: int = 800) -> dict[str, list[str]]:
    """
    Load all .txt and .md files under 'path' (non-recursive for now),
    return a mapping: { doc_id -> [chunks...] }.
    """
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Path does not exist or is not a directory: {path}")

    doc_chunks: dict[str, list[str]] = {}

    for file_path in sorted(path.iterdir()):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in {".txt", ".md"}:
            continue

        text = load_text_file(file_path)
        chunks = simple_chunk_text(text, max_chars=max_chars)
        if not chunks:
            continue

        doc_id = file_path.stem  # filename without extension
        doc_chunks[doc_id] = chunks

    return doc_chunks
