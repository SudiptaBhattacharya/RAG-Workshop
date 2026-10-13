# Setup guide

Use this guide when preparing the facilitator machine or student laptops. Complete the facilitator setup at least one day before the workshop and repeat the preflight on the day.

## 1. Hardware, software, and access

Recommended:

- macOS, Windows 10/11, or a current Linux distribution.
- 8 GB RAM minimum; 16 GB is more comfortable.
- Approximately 4 GB of free disk space for Python packages and model caches.
- Internet access during initial installation and for live Groq/API demonstrations.
- A modern browser.
- A free Groq account and API key only if live generation is required.

The workshop uses Python 3.12. Do not use this machine's system Python 3.14 for the project.

## 2. Install `uv`

Choose one method. Restart the terminal afterward if `uv --version` is not immediately available.

### macOS with Homebrew

```bash
brew install uv
```

### macOS or Linux installer

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows PowerShell

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:

```bash
uv --version
```

## 3. Create the environment

Open a terminal in the project directory, then run:

```bash
uv python install 3.12
uv sync
```

`uv sync` creates `.venv` and installs both the application and development dependencies. Do not install packages globally.

## 4. Configure secrets

Offline mode needs no secrets. For live generated answers:

### macOS or Linux

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Open `.env` and add:

```dotenv
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

The model name is configurable because hosted model availability changes. If Groq retires the default, choose an active chat-completion model in the Groq console and update `GROQ_MODEL`.

Security rules:

- Never paste an API key into workshop slides, chat, or source code.
- Never commit `.env` or `.streamlit/secrets.toml`.
- Use a dedicated workshop key and rotate/revoke it afterward if it was shared.
- Review the provider's current usage limits before teaching.

## 5. Pre-download and verify

Run:

```bash
uv run python scripts/preflight.py
uv run python scripts/warmup.py
uv run pytest
```

The warm-up downloads and caches `sentence-transformers/all-MiniLM-L6-v2`, creates embeddings for the sample corpus, and performs one test retrieval. Run it on every presentation machine and student image before the session.

## 6. Start the workshop app

```bash
uv run streamlit run app.py
```

If the browser does not open automatically, visit:

```text
http://localhost:8501
```

Stop the app with `Ctrl+C` in the terminal.

## 6A. Prepare each student's rebuild file

Students should work in a personal copy, leaving the starter and reference files unchanged:

### macOS or Linux

```bash
cp student_lab/rag_starter.py student_lab/my_rag.py
```

### Windows PowerShell

```powershell
Copy-Item student_lab/rag_starter.py student_lab/my_rag.py
```

Confirm the complete reference pipeline works once:

```bash
uv run python student_lab/rag_walkthrough.py
```

The workshop app's `0 · RAG code walkthrough` section reveals the matching implementation one function at a time. Detailed milestones are in `student_lab/README.md`.

## 7. Start the MCP demonstration

The MCP portion is independent of Streamlit. The easiest live demonstration uses the official Inspector:

```bash
uv run mcp dev mcp_server.py
```

In the Inspector:

1. List resources.
2. Read `workshop://documents/sales-report`.
3. List tools.
4. Call `prepare_ticket_draft` with a title, evidence, and severity.
5. Inspect `data/output/ticket_draft.json`.

For a terminal-only demonstration:

```bash
uv run python mcp_demo_client.py
```

The tool creates a local draft only. It intentionally stops before any external API action.

## 8. Student installation options

### Recommended: paired local setup

- Students install `uv` before the workshop.
- Provide the project folder or repository link.
- Ask them to run `uv sync` and `scripts/warmup.py` before arriving.
- Put students in pairs so one machine can continue if another has an environment problem.

### Low-friction: facilitator-led demonstration

- Run the application on the facilitator machine.
- Students make predictions and interpret results using the shared display.
- Share the repository afterward for independent exploration.

### Cloud deployment

The included `requirements.txt` supports Streamlit Community Cloud:

1. Push the project to a GitHub repository.
2. Create a Streamlit Community Cloud app with `app.py` as the entry point.
3. Add `GROQ_API_KEY`, `GROQ_MODEL`, and `EMBEDDING_MODEL` in the app's Secrets settings if live generation is desired.
4. Reboot the app after changing secrets.

Cloud cold starts can be slow because the embedding model must download. Test the deployment before sharing it.

## 9. Using your own documents

Upload PDF, TXT, or Markdown files from the sidebar. PDFs must contain selectable text. Scanned PDFs require OCR before the workshop application can parse them.

For a controlled lesson, begin with the included fictional documents. They contain deliberately known facts, so retrieval and grounding can be evaluated objectively.

## 10. Troubleshooting

### `uv` is not found

Restart the terminal. If the problem persists, follow the PATH instructions printed by the installer or use the Homebrew installation on macOS.

### Python 3.14 package errors

Confirm the project environment rather than system Python is active:

```bash
uv run python --version
```

It should report Python 3.12.x.

### Embedding download is slow or blocked

- Run `scripts/warmup.py` on an unrestricted network in advance.
- Keep the facilitator's model cache intact.
- If student devices cannot download models, use the facilitator-led format.

### Groq authentication or model error

- Confirm `.env` is in the project root.
- Confirm the key has no quotes or trailing spaces.
- Check the active model list in the Groq console and update `GROQ_MODEL`.
- Remove the key temporarily to continue in offline grounded-demo mode.

### PDF produces no text

The PDF is probably scanned. Use an OCR tool first or export the content as TXT.

### Port 8501 is already in use

```bash
uv run streamlit run app.py --server.port 8502
```

### MCP Inspector cannot start

Confirm `uv sync` completed, then check:

```bash
uv run mcp version
uv run python mcp_demo_client.py
```

The terminal client proves the server independently of the Inspector UI.

## 11. Day-of fallback kit

Keep these available:

- A fully warmed facilitator laptop.
- The repository as a local zip/archive.
- Screenshots of each experiment's expected output.
- Offline mode tested with no `.env` file.
- A local copy of the sample documents.
- A second browser profile and a spare port.
- The ticket-draft demonstration, which requires no Jira account.
