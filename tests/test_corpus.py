from rag_workshop.corpus import extract_document, load_sample_corpus


def test_sample_corpus_loads_expected_documents() -> None:
    pages = load_sample_corpus()
    sources = {page.source for page in pages}
    assert sources == {"atlas_memo.txt", "sales_report.txt", "lecture_notes.txt"}
    assert len(pages) >= 7


def test_text_upload_honours_page_breaks() -> None:
    pages = extract_document("notes.txt", b"page one\fpage two")
    assert [page.page for page in pages] == [1, 2]
