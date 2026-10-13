from rag_workshop.chunking import chunk_pages
from rag_workshop.corpus import load_sample_corpus
from rag_workshop.retrieval import keyword_search


def test_keyword_search_finds_atlas_budget() -> None:
    chunks = chunk_pages(load_sample_corpus(), chunk_size=500, overlap=100)
    results = keyword_search("Project Atlas budget cap", chunks, top_k=3)
    assert results
    assert "42,000" in " ".join(result.chunk.text for result in results)
