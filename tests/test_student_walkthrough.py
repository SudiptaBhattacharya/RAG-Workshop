from student_lab.rag_walkthrough import DOCUMENT, build_prompt, chunk_pages, load_pages


def test_student_pipeline_loads_and_chunks() -> None:
    pages = load_pages(DOCUMENT)
    chunks = chunk_pages(pages, size=500, overlap=100)
    assert len(pages) == 2
    assert len(chunks) >= 3
    assert all({"id", "source", "page", "text"} <= chunk.keys() for chunk in chunks)


def test_student_prompt_contains_question_evidence_and_citation() -> None:
    hits = [
        {
            "source": "memo.txt",
            "page": 2,
            "text": "The cap is AUD 42,000.",
            "score": 0.9,
        }
    ]
    prompt = build_prompt("What is the cap?", hits)
    assert "What is the cap?" in prompt
    assert "AUD 42,000" in prompt
    assert "memo.txt, p. 2" in prompt
