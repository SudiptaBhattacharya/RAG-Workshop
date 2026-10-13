from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from .embeddings import embed_texts
from .models import Chunk, SearchResult


def _rank(chunks: list[Chunk], scores: np.ndarray, top_k: int, method: str) -> list[SearchResult]:
    if not chunks:
        return []
    indices = np.argsort(scores)[::-1][: max(1, min(top_k, len(chunks)))]
    return [
        SearchResult(chunk=chunks[int(index)], score=float(scores[index]), rank=rank, method=method)
        for rank, index in enumerate(indices, start=1)
    ]


def keyword_search(query: str, chunks: list[Chunk], top_k: int = 4) -> list[SearchResult]:
    if not chunks:
        return []
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([chunk.text for chunk in chunks] + [query])
    scores = (matrix[:-1] @ matrix[-1].T).toarray().ravel()
    return _rank(chunks, scores, top_k, "keyword")


def vector_search(
    query: str,
    chunks: list[Chunk],
    top_k: int = 4,
    chunk_vectors: np.ndarray | None = None,
) -> tuple[list[SearchResult], np.ndarray]:
    if not chunks:
        return [], np.empty((0, 0), dtype=np.float32)
    vectors = chunk_vectors if chunk_vectors is not None else embed_texts([c.text for c in chunks])
    query_vector = embed_texts([query])[0]
    scores = vectors @ query_vector
    return _rank(chunks, scores, top_k, "vector"), vectors


def hybrid_search(
    query: str,
    chunks: list[Chunk],
    top_k: int = 4,
    chunk_vectors: np.ndarray | None = None,
    semantic_weight: float = 0.7,
) -> tuple[list[SearchResult], np.ndarray]:
    keyword = keyword_search(query, chunks, top_k=len(chunks))
    vector, vectors = vector_search(query, chunks, top_k=len(chunks), chunk_vectors=chunk_vectors)
    keyword_scores = {item.chunk.chunk_id: item.score for item in keyword}
    vector_scores = {item.chunk.chunk_id: item.score for item in vector}
    combined = np.array(
        [
            semantic_weight * vector_scores[chunk.chunk_id]
            + (1 - semantic_weight) * keyword_scores[chunk.chunk_id]
            for chunk in chunks
        ]
    )
    return _rank(chunks, combined, top_k, "hybrid"), vectors
