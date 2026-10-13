from __future__ import annotations

import importlib
import os
import platform
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "streamlit",
    "sentence_transformers",
    "sklearn",
    "plotly",
    "pdfplumber",
    "groq",
    "mcp",
]


def main() -> int:
    print("AI Architecture Workshop preflight")
    print(f"Project: {PROJECT_ROOT}")
    print(f"Python: {sys.version.split()[0]} ({platform.machine()})")
    failures: list[str] = []
    if not ((3, 11) <= sys.version_info[:2] < (3, 14)):
        failures.append("Use Python 3.11, 3.12, or 3.13; Python 3.12 is recommended.")

    for module in REQUIRED:
        try:
            imported = importlib.import_module(module)
            version = getattr(imported, "__version__", "installed")
            print(f"[ok] {module}: {version}")
        except Exception as error:  # noqa: BLE001 - diagnostics should report every import failure
            failures.append(f"{module}: {error}")

    for filename in ("atlas_memo.txt", "sales_report.txt", "lecture_notes.txt"):
        path = PROJECT_ROOT / "data" / "sample" / filename
        if path.exists():
            print(f"[ok] sample data: {filename}")
        else:
            failures.append(f"Missing sample data: {path}")

    if os.getenv("GROQ_API_KEY"):
        print("[ok] GROQ_API_KEY is set (value not displayed)")
    else:
        print("[optional] GROQ_API_KEY is not set; offline grounded-demo mode will be used")

    if failures:
        print("\nPreflight failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("\nPreflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
