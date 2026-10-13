from __future__ import annotations

from collections import Counter

import numpy as np
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

from .embeddings import embed_texts
from .models import Chunk


def top_keywords(chunks: list[Chunk], limit: int = 30) -> list[dict[str, float | str]]:
    if not chunks:
        return []
    vectorizer = TfidfVectorizer(stop_words="english", max_features=500, ngram_range=(1, 1))
    matrix = vectorizer.fit_transform([chunk.text for chunk in chunks])
    scores = np.asarray(matrix.mean(axis=0)).ravel()
    terms = vectorizer.get_feature_names_out()
    ranked = np.argsort(scores)[::-1][:limit]
    return [{"term": str(terms[index]), "score": float(scores[index])} for index in ranked]


def keyword_network(chunks: list[Chunk], limit: int = 30) -> dict[str, list[dict]]:
    terms = [str(item["term"]) for item in top_keywords(chunks, limit=limit)]
    if not terms:
        return {"nodes": [], "edges": []}

    vectors = embed_texts(terms)
    positions = PCA(n_components=2, random_state=42).fit_transform(vectors)
    scale = np.max(np.abs(positions), axis=0)
    scale[scale == 0] = 1
    positions = positions / scale

    lower_chunks = [chunk.text.lower() for chunk in chunks]
    frequencies = Counter()
    cooccurrence = Counter()
    for text in lower_chunks:
        present = [term for term in terms if term in text]
        for term in present:
            frequencies[term] += text.count(term)
        for i, left in enumerate(present):
            for right in present[i + 1 :]:
                cooccurrence[tuple(sorted((left, right)))] += 1

    similarities = vectors @ vectors.T
    edges: list[dict] = []
    for i, left in enumerate(terms):
        candidates = np.argsort(similarities[i])[::-1][1:4]
        for j in candidates:
            right = terms[int(j)]
            key = tuple(sorted((left, right)))
            if similarities[i, j] >= 0.35 or cooccurrence[key] >= 2:
                edge = {
                    "source": left,
                    "target": right,
                    "similarity": float(similarities[i, j]),
                    "cooccurrence": int(cooccurrence[key]),
                }
                reverse_key = (edge["target"], edge["source"])
                if not any((e["source"], e["target"]) == reverse_key for e in edges):
                    edges.append(edge)

    nodes = [
        {
            "term": term,
            "x": float(positions[index, 0]),
            "y": float(positions[index, 1]),
            "frequency": int(frequencies[term]),
        }
        for index, term in enumerate(terms)
    ]
    return {"nodes": nodes, "edges": edges}
