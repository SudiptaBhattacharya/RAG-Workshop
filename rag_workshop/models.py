from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    source: str
    page: int
    text: str


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source: str
    page: int
    text: str
    start: int
    end: int

    @property
    def citation(self) -> str:
        return f"{self.source}, p. {self.page}"


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float
    rank: int
    method: str
