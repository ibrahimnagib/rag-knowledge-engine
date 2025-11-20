from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import chromadb
from chromadb.config import Settings

from .config import config
from .embeddings import embed_texts


@dataclass
class StoredChunk:
    doc_id: str
    text: str


class VectorStore:
    """
    ChromaDB-based vector store.

    Each index_name corresponds to a Chroma collection with:
      - embeddings stored on disk in data/indexes/
      - metadata per chunk: { "doc_id": ..., "text": ... }
    """

    def __init__(self, index_name: str, dim: int = 1536):
        self.index_name = index_name
        self.dim = dim

        # Ensure base directory exists
        config.indexes_dir.mkdir(parents=True, exist_ok=True)

        # Chroma will manage files under this directory
        self._client = chromadb.PersistentClient(
            path=str(config.indexes_dir),
            settings=Settings(
                anonymized_telemetry=False,
            ),
        )

        # One collection per logical index
        self._collection = self._client.get_or_create_collection(
            name=index_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_texts(self, doc_id: str, texts: List[str]) -> None:
        """
        Add multiple text chunks under a single doc_id.
        """
        if not texts:
            return

        # Compute embeddings using our OpenAI-based helper
        vectors = embed_texts(texts)  # List[List[float]]

        # Chroma requires distinct ids per record
        ids = [
            f"{doc_id}_{i}_{len(self._collection.get()['ids']) if self._collection.count() else 0}"
            for i in range(len(texts))
        ]

        metadatas = [{"doc_id": doc_id} for _ in texts]

        self._collection.add(
            ids=ids,
            documents=texts,
            embeddings=vectors,
            metadatas=metadatas,
        )

    def similarity_search(self, query: str, top_k: int = 5) -> List[Tuple[StoredChunk, float]]:
        """
        Embed the query, search the index, return top_k (chunk, score) pairs.
        """
        if self._collection.count() == 0:
            return []

        query_embeddings = embed_texts([query])

        result = self._collection.query(
            query_embeddings=query_embeddings,
            n_results=top_k,
        )

        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        scores = result.get("distances", [[]])[0]  # for cosine, lower is closer; we can invert

        out: List[Tuple[StoredChunk, float]] = []
        for doc_text, meta, dist in zip(documents, metadatas, scores):
            doc_id = meta.get("doc_id", "unknown")
            # Convert distance-like value into a similarity score in [0, 1]
            # Here we'll just do a simple transform: score = 1 / (1 + dist)
            similarity = 1.0 / (1.0 + float(dist))
            out.append(
                (StoredChunk(doc_id=doc_id, text=doc_text), similarity)
            )

        return out

def list_indexes() -> list[dict]:
        """
        List all Chroma collections (indexes) with basic metadata.
        """
        # Reuse the same base directory as VectorStore
        client = chromadb.PersistentClient(
            path=str(config.indexes_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        collections = client.list_collections()

        result: list[dict] = []
        for col in collections:
            meta = col.metadata or {}
            index_id = col.name
            display_name = meta.get("display_name", index_id.replace("_", " ").title())
            result.append(
                {
                    "id": index_id,
                    "name": display_name,
                    "metadata": meta,
                }
            )
        return result

def list_docs_in_index(index_name: str) -> list[str]:
    """
    Return a de-duplicated list of doc_ids stored in a given index (collection).
    """
    store = VectorStore(index_name=index_name)
    # Pull all metadatas; for small personal projects this is fine
    data = store._collection.get(include=["metadatas"])

    metadatas = data.get("metadatas") or []
    doc_ids: set[str] = set()

    # metadatas may be a flat list or list-of-lists depending on version
    for entry in metadatas:
        if isinstance(entry, list):
            for m in entry:
                if m and isinstance(m, dict) and "doc_id" in m:
                    doc_ids.add(str(m["doc_id"]))
        elif isinstance(entry, dict) and "doc_id" in entry:
            doc_ids.add(str(entry["doc_id"]))

    return sorted(doc_ids)