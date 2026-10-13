from __future__ import annotations

from .models import Chunk, Page


def chunk_pages(pages: list[Page], chunk_size: int = 500, overlap: int = 100) -> list[Chunk]:
    if chunk_size < 50:
        raise ValueError("chunk_size must be at least 50 characters")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    chunks: list[Chunk] = []
    chunk_number = 1
    for page in pages:
        text = " ".join(page.text.split())
        start = 0
        while start < len(text):
            proposed_end = min(start + chunk_size, len(text))
            end = proposed_end
            if proposed_end < len(text):
                boundary = text.rfind(" ", start + int(chunk_size * 0.65), proposed_end)
                if boundary > start:
                    end = boundary
            snippet = text[start:end].strip()
            if snippet:
                chunks.append(
                    Chunk(
                        chunk_id=f"C{chunk_number:03d}",
                        source=page.source,
                        page=page.page,
                        text=snippet,
                        start=start,
                        end=end,
                    )
                )
                chunk_number += 1
            if end >= len(text):
                break
            start = max(end - overlap, start + 1)
    return chunks
