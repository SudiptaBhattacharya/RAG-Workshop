# AI Architecture Workshop

A runnable, first-principles workshop that teaches APIs, embeddings, retrieval-augmented generation (RAG), evaluation, and Model Context Protocol (MCP) through nine cumulative experiments.

The project is offline-first. Every experiment runs without a paid service; a Groq key optionally enables live generated answers.

## Quick start

From this directory:

```bash
uv python install 3.12
uv sync
uv run python scripts/preflight.py
uv run python scripts/warmup.py
uv run streamlit run app.py
```

The first warm-up downloads the public `all-MiniLM-L6-v2` embedding model. Streamlit then opens the workshop in a browser, normally at `http://localhost:8501`.

Students can run the small reference implementation directly:

```bash
uv run python student_lab/rag_walkthrough.py
```

To enable live Groq generation:

```bash
cp .env.example .env
```

Add `GROQ_API_KEY` to `.env`. Never commit that file.

## What is included

- One Streamlit application covering all nine experiments.
- Three small fictional documents with known ground truth.
- PDF, TXT, and Markdown upload support.
- Character chunking with source/page metadata.
- Sentence-transformer embeddings and cosine similarity.
- Keyword, vector, and hybrid retrieval.
- A top-30 TF-IDF keyword map with semantic positions and relationship edges.
- Offline grounded-demo mode and optional Groq generation.
- A real local MCP server with resources and a safe ticket-draft tool.
- Preflight, model warm-up, automated tests, and a facilitator runbook.

## Documentation

- [Detailed installation and troubleshooting](SETUP.md)
- [Start-to-end facilitation script](WORKSHOP_RUNBOOK.md)
- [Architecture and teaching decisions](ARCHITECTURE.md)
- [Student rebuild lab](student_lab/README.md)

## Verify the project

```bash
uv run pytest
uv run ruff check .
```

## Run the MCP demonstration

Open the MCP Inspector:

```bash
uv run mcp dev mcp_server.py
```

Or run the included in-process client:

```bash
uv run python mcp_demo_client.py
```

The `prepare_ticket_draft` tool only writes `data/output/ticket_draft.json`. It never contacts Jira or another external service.
