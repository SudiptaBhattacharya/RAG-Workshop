"""Student starter: implement the five RAG stages marked TODO."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from groq import Groq  # noqa: F401 - used when students complete STEP 5B
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT = ROOT / "data" / "sample" / "atlas_memo.txt"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_model: SentenceTransformer | None = None


def load_pages(path: Path) -> list[dict]:
    """STEP 1: read text, split on \f, and preserve source/page metadata."""
    # TODO: return dictionaries with source, page, and text.
    raise NotImplementedError("Complete STEP 1: load_pages")


def chunk_pages(pages: list[dict], size: int = 500, overlap: int = 100) -> list[dict]:
    """STEP 2: create overlapping chunks with id/source/page/text."""
    # TODO: move a [start:end] window through every page.
    raise NotImplementedError("Complete STEP 2: chunk_pages")


def embedding_model() -> SentenceTransformer:
    """Helper: load the embedding model once."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_chunks(chunks: list[dict]) -> np.ndarray:
    """STEP 3: encode chunk text as normalized embeddings."""
    # TODO: call embedding_model().encode(..., normalize_embeddings=True).
    raise NotImplementedError("Complete STEP 3: embed_chunks")


def retrieve(
    question: str,
    chunks: list[dict],
    chunk_vectors: np.ndarray,
    top_k: int = 3,
) -> list[dict]:
    """STEP 4: embed the question, score every chunk, and return top-k."""
    # TODO: cosine similarity is a dot product because vectors are normalized.
    raise NotImplementedError("Complete STEP 4: retrieve")


def build_prompt(question: str, hits: list[dict]) -> str:
    """STEP 5A: combine instructions, question, evidence, and citations."""
    # TODO: join the hit text and metadata into one grounded prompt.
    raise NotImplementedError("Complete STEP 5A: build_prompt")


def generate_answer(question: str, hits: list[dict]) -> str:
    """STEP 5B: send the grounded prompt to Groq or return it offline."""
    prompt = build_prompt(question, hits)
    if not os.getenv("GROQ_API_KEY"):
        return "OFFLINE MODE — this is the exact grounded prompt:\n\n" + prompt

    # TODO: call Groq().chat.completions.create(...) with a low temperature.
    raise NotImplementedError("Complete STEP 5B: Groq generation")


def run_rag(question: str, document: Path = DOCUMENT) -> tuple[str, list[dict]]:
    """Connect the five stages after implementing them."""
    pages = load_pages(document)
    chunks = chunk_pages(pages)
    vectors = embed_chunks(chunks)
    hits = retrieve(question, chunks, vectors)
    return generate_answer(question, hits), hits


if __name__ == "__main__":
    load_dotenv(ROOT / ".env")
    user_question = input("Question: ").strip() or "What is the Project Atlas budget cap?"
    answer, evidence = run_rag(user_question)
    print("\nRetrieved evidence:")
    for hit in evidence:
        print(f"- score={hit['score']:.3f} [{hit['source']}, p. {hit['page']}]")
    print("\nAnswer:\n" + answer)
