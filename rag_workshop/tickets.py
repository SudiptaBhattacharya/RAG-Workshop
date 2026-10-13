from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"


def create_ticket_draft(
    title: str,
    evidence: str,
    severity: str = "medium",
    save: bool = False,
) -> dict[str, str]:
    if severity not in {"low", "medium", "high"}:
        raise ValueError("severity must be low, medium, or high")
    if not title.strip() or not evidence.strip():
        raise ValueError("title and evidence are required")
    draft = {
        "title": title.strip(),
        "evidence": evidence.strip(),
        "severity": severity,
        "status": "draft_requires_human_approval",
        "created_at": datetime.now(UTC).isoformat(),
    }
    if save:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUTPUT_DIR / "ticket_draft.json").write_text(json.dumps(draft, indent=2), encoding="utf-8")
    return draft
