from __future__ import annotations

from rag_workshop.chunking import chunk_pages
from rag_workshop.corpus import load_sample_corpus
from rag_workshop.embeddings import embed_texts
from rag_workshop.retrieval import vector_search


def main() -> None:
    pages = load_sample_corpus()
    chunks = chunk_pages(pages, chunk_size=500, overlap=100)
    print(f"Loaded {len(pages)} pages and created {len(chunks)} chunks.")
    print("Downloading/loading the embedding model. The first run can take several minutes…")
    vectors = embed_texts([chunk.text for chunk in chunks])
    results, _ = vector_search(
        "What is the Project Atlas spending limit?",
        chunks,
        top_k=3,
        chunk_vectors=vectors,
    )
    print(f"Embedding matrix: {vectors.shape}")
    for result in results:
        print(
            f"#{result.rank} score={result.score:.3f} "
            f"{result.chunk.citation}: {result.chunk.text[:90]}…"
        )
    print("Warm-up complete. The model is cached for the workshop.")


if __name__ == "__main__":
    main()
