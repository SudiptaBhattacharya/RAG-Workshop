from __future__ import annotations

import os
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=2)
def get_embedding_model(model_name: str | None = None) -> SentenceTransformer:
    selected = model_name or os.getenv("EMBEDDING_MODEL", DEFAULT_MODEL)
    return SentenceTransformer(selected)


def embed_texts(texts: list[str], model_name: str | None = None) -> np.ndarray:
    if not texts:
        return np.empty((0, 0), dtype=np.float32)
    model = get_embedding_model(model_name)
    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return np.asarray(vectors, dtype=np.float32)


def cosine_matrix(vectors: np.ndarray) -> np.ndarray:
    if vectors.ndim != 2:
        raise ValueError("vectors must be a two-dimensional array")
    return vectors @ vectors.T
