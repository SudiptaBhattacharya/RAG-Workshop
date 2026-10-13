from __future__ import annotations

import io
from pathlib import Path

import pdfplumber

from .models import Page

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = PROJECT_ROOT / "data" / "sample"


def _text_to_pages(source: str, text: str) -> list[Page]:
    parts = [part.strip() for part in text.split("\f") if part.strip()]
    return [Page(source=source, page=index + 1, text=part) for index, part in enumerate(parts)]


def load_text_file(path: Path) -> list[Page]:
    return _text_to_pages(path.name, path.read_text(encoding="utf-8"))


def load_sample_corpus() -> list[Page]:
    pages: list[Page] = []
    for filename in ("atlas_memo.txt", "sales_report.txt", "lecture_notes.txt"):
        pages.extend(load_text_file(SAMPLE_DIR / filename))
    return pages


def extract_document(name: str, data: bytes) -> list[Page]:
    suffix = Path(name).suffix.lower()
    if suffix == ".pdf":
        pages: list[Page] = []
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for index, pdf_page in enumerate(pdf.pages):
                text = (pdf_page.extract_text() or "").strip()
                if text:
                    pages.append(Page(source=name, page=index + 1, text=text))
        if not pages:
            raise ValueError(
                "No selectable text was found. This may be a scanned PDF; run OCR first."
            )
        return pages
    if suffix in {".txt", ".md"}:
        return _text_to_pages(name, data.decode("utf-8"))
    raise ValueError("Supported uploads are PDF, TXT, and Markdown files.")


def corpus_summary(pages: list[Page]) -> dict[str, int]:
    return {
        "documents": len({page.source for page in pages}),
        "pages": len(pages),
        "characters": sum(len(page.text) for page in pages),
        "words": sum(len(page.text.split()) for page in pages),
    }
