from rag_workshop.chunking import chunk_pages
from rag_workshop.models import Page


def test_chunking_preserves_metadata_and_overlap() -> None:
    page = Page(source="demo.txt", page=3, text="word " * 300)
    chunks = chunk_pages([page], chunk_size=200, overlap=50)
    assert len(chunks) > 1
    assert all(chunk.source == "demo.txt" and chunk.page == 3 for chunk in chunks)
    assert chunks[1].start < chunks[0].end


def test_overlap_must_be_smaller_than_chunk() -> None:
    page = Page(source="demo.txt", page=1, text="hello world")
    try:
        chunk_pages([page], chunk_size=100, overlap=100)
    except ValueError as error:
        assert "smaller" in str(error)
    else:
        raise AssertionError("Expected ValueError")
