# RAG Workshop: Complete Show-and-Run Guide

## 1. Workshop files

Use these files during delivery:

- Slide deck: `deliverables/RAG_Workshop_Student_Deck_v1.pptx`
- Slide and demonstration script: `deliverables/RAG_WORKSHOP_TEACHING_SCRIPT.md`
- Workshop application: `app.py`
- Student setup and milestones: `student_lab/README.md`
- Student starter: `student_lab/rag_starter.py`
- Complete student reference: `student_lab/rag_walkthrough.py`
- MCP server: `mcp_server.py`
- MCP terminal client: `mcp_demo_client.py`
- Detailed setup reference: `SETUP.md`
- Timed facilitator reference: `WORKSHOP_RUNBOOK.md`

The verified configuration uses Python 3.12.15. The application also supports Python 3.11 and 3.13, but not Python 3.14.

## 2. Select a delivery mode

### Mode A: facilitator laptop

Run the slides, Streamlit application, and optional MCP demonstration on one prepared computer. This is the recommended mode because students can participate without installing the complete environment during the session.

### Mode B: student local build

Each student installs the project and implements the five RAG functions in `student_lab/my_rag.py`. Use pairs so that one working computer can support two students.

### Mode C: hosted demonstration

Deploy `app.py` to Streamlit Community Cloud and place its URL in the optional demonstration QR code. Students can still download the project and complete the five-function build locally.

### Mode D: offline presentation

Use the PowerPoint deck and the offline application mode. Live generation is optional because the application can display retrieved evidence and the exact grounded prompt without an API key.

## 3. Install the facilitator environment

Open a terminal in the project directory:

```bash
cd "/Users/evam/Documents/ChatGPT/RAG"
```

Install `uv` if it is not already available.

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

Install Python 3.12 and the locked dependencies:

```bash
uv python install 3.12
uv sync
```

Do not install workshop packages into the system Python environment.

## 4. Configure optional live generation

The workshop runs without an API key. Complete this section only if live Groq generation is required.

### macOS or Linux

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Add the following values to `.env`:

```dotenv
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Confirm that the selected model is active in the provider console before the workshop. Never display, commit, or distribute the API key.

## 5. Prepare the machine before the workshop

Run these commands while internet access is available:

```bash
uv run python scripts/preflight.py
uv run python scripts/warmup.py
uv run pytest
uv run ruff check .
```

Expected results:

- Preflight reports `Preflight passed.`
- Warm-up creates an embedding matrix and retrieves the Atlas evidence.
- Pytest reports nine passing tests.
- Ruff reports no lint errors.

The warm-up downloads and caches `sentence-transformers/all-MiniLM-L6-v2`. Preserve that cache for offline delivery.

## 6. Prepare the slides and QR codes

Open `deliverables/RAG_Workshop_Student_Deck_v1.pptx` in PowerPoint, Keynote, or LibreOffice Impress. Use presenter view so that the speaker notes remain visible only to the instructor.

Slide 16 contains two editable placeholders:

1. Replace `Workshop files` with a QR code for the repository, shared folder, or downloadable archive.
2. Replace `Optional hosted demo` with a QR code for the deployed Streamlit application, or delete this block when no hosted demonstration is used.

Test both QR codes with a separate phone and a student-level account. Do not use a link that requires instructor credentials.

## 7. Start the teaching application

Run:

```bash
uv run streamlit run app.py
```

Open the displayed address, normally:

```text
http://localhost:8501
```

If port 8501 is occupied, use:

```bash
uv run streamlit run app.py --server.port 8502
```

Stop the application with `Ctrl+C` in its terminal.

## 8. Configure the application before students arrive

Use these initial control values:

- Chunk size: `500`
- Overlap: `100`
- Retrieved chunks: `4`
- Retrieval: `hybrid`
- Corpus: included sample documents

Open each experiment once so the model and application caches are populated. Return to `0 · RAG code walkthrough` before the session begins.

Keep the slide deck and browser in separate windows. Use the slide deck for the concept, then switch to the browser for the corresponding observation.

## 9. Run the slide and demonstration sequence

Use `deliverables/RAG_WORKSHOP_TEACHING_SCRIPT.md` for the exact spoken text.

| Slides | Demonstration | Operation |
|---|---|---|
| 1–2 | No execution | Introduce the five-function build and the evaluation objective. |
| 3 | Experiment 1 | Ask the Atlas question without the Atlas memo, collect a prediction, then select `Run baseline`. |
| 4 | RAG code walkthrough | Select `Run all five stages` and identify the object passed across each stage. |
| 5 | RAG code walkthrough | Select `load_pages` and inspect the source, page, and text fields. |
| 6–7 | Experiment 3 | Compare chunk size `150`, overlap `0` with chunk size `500`, overlap `100`. |
| 8 | Experiment 4 | Compare two paraphrases with one unrelated sentence and inspect cosine similarity. |
| 9 | Experiment 4 | Display the top-30 keyword network and identify position, node size, and edges. |
| 10 | Experiment 5 | Run the paraphrased Atlas query through keyword and vector retrieval and compare rankings. |
| 11 | RAG code walkthrough | Display the grounded prompt and identify the question, evidence, citations, and refusal rule. |
| 12 | Experiment 6 | Select `Run both conditions` and compare no-context output with retrieved-context output. |
| 13 | Experiment 7 | Run no overlap, low or high top-k, an unanswerable question, and retrieved prompt injection. |
| 14 | Experiments 2 and 8 | Show the API request envelope, then compare an MCP resource with an MCP tool. |
| 15 | Experiment 9 | Select `Run the relay` and inspect RAG evidence, model synthesis, tool arguments, and approval. |
| 16 | Student files | Display the QR code and direct students to create their personal working file. |

## 10. Use the controlled example questions

Use these questions in order:

```text
When does Project Atlas launch and what is its budget cap?
```

Expected evidence: launch on 17 November 2026 and an approved spending cap of AUD 42,000.

```text
Why does the implementation use overlapping chunks?
```

Expected evidence: overlap keeps an idea intact when a sentence or explanation falls near a chunk boundary.

```text
What colour is the Project Atlas office carpet?
```

Expected result: the system should report insufficient evidence rather than invent an answer.

For the MCP relay, use the sales report facts:

```text
Target AUD 1,200,000; actual AUD 1,050,000; shortfall AUD 150,000.
```

## 11. Run the student build

Students first create a personal copy.

### macOS or Linux

```bash
cp student_lab/rag_starter.py student_lab/my_rag.py
```

### Windows PowerShell

```powershell
Copy-Item student_lab/rag_starter.py student_lab/my_rag.py
```

Students implement the following functions in order:

1. `load_pages`
2. `chunk_pages`
3. `embed_chunks`
4. `retrieve`
5. `build_prompt` and `generate_answer`

Run the student file after each milestone:

```bash
uv run python student_lab/my_rag.py
```

Run the complete readable reference when a comparison is required:

```bash
uv run python student_lab/rag_walkthrough.py
```

Students should verify:

- Page records preserve source and page metadata.
- Chunks have unique identifiers and visible overlap.
- The embedding matrix has one normalized 384-dimensional vector per chunk.
- Retrieval scores are sorted from highest to lowest.
- The prompt includes evidence, citations, and an insufficient-evidence instruction.

## 12. Run the MCP demonstration

### Browser-based Inspector

Start the official MCP Inspector:

```bash
uv run mcp dev mcp_server.py
```

In the Inspector:

1. List resources.
2. Read `workshop://documents/sales-report`.
3. List tools.
4. Call `prepare_ticket_draft`.
5. Use title `Review quarterly revenue shortfall`.
6. Use evidence `Target AUD 1,200,000; actual AUD 1,050,000; shortfall AUD 150,000.`
7. Use severity `medium`.
8. Inspect `data/output/ticket_draft.json`.

### Terminal-only alternative

Run:

```bash
uv run python mcp_demo_client.py
```

The demonstration creates a local draft only. It does not contact Jira or another external system.

## 13. Deploy an optional hosted demonstration

The repository includes `requirements.txt` for Streamlit Community Cloud.

1. Publish the project to a repository that the deployment service can access.
2. Create a Streamlit Community Cloud application.
3. Set `app.py` as the entry point.
4. Add `GROQ_API_KEY`, `GROQ_MODEL`, and `EMBEDDING_MODEL` in the deployment secrets only when live generation is required.
5. Reboot the application after changing secrets.
6. Test every experiment after a cold start.
7. Place the deployed URL in the optional QR code on slide 16.

The embedding model downloads during a cold start, so launch and test the hosted application before students scan the QR code.

## 14. Use student documents

The application accepts PDF, TXT, and Markdown files through the sidebar. PDFs must contain selectable text; scanned PDFs require optical character recognition before upload.

Begin with the included fictional documents because their ground truth is known. After the controlled experiments, students may upload a short document and test one answerable and one unanswerable question.

## 15. Recovery procedures

### Live model request fails

Remove or ignore `GROQ_API_KEY` and continue in offline grounded-prompt mode. The retrieval and evidence-inspection objectives remain available.

### Internet access fails

Use the cached embedding model, sample documents, offline generation mode, local slides, and terminal MCP client.

### Retrieval output is unexpected

Reset chunk size to `500`, overlap to `100`, top-k to `4`, retrieval to `hybrid`, and corpus to the included sample documents.

### Port 8501 is unavailable

```bash
uv run streamlit run app.py --server.port 8502
```

### A student cannot install the environment

Pair the student with a working machine and continue with the shared demonstration. Do not use teaching time to repair system Python or a restricted corporate proxy.

### The embedding model cannot download

Use the warmed facilitator machine. Run `scripts/warmup.py` on an unrestricted network before the next session.

### Groq authentication or model selection fails

Confirm that `.env` is in the project root, verify that the key has no quotes or trailing spaces, and select a currently available model in `GROQ_MODEL`.

### A PDF produces no text

Use an OCR-processed PDF or export the content as TXT.

### MCP Inspector fails

Verify the installation and use the terminal fallback:

```bash
uv run mcp version
uv run python mcp_demo_client.py
```

## 16. End the workshop

1. Stop Streamlit and MCP processes with `Ctrl+C`.
2. Delete or rotate any shared API key.
3. Remove `data/output/ticket_draft.json` if it is no longer required.
4. Collect failed questions as candidates for a retrieval evaluation dataset.
5. Preserve the working project, model cache, slide deck, and teaching script for the next delivery.

## 17. Final day-of checklist

- [ ] Slide deck opens and presenter notes are visible.
- [ ] Workshop-files QR code works from a student device.
- [ ] Optional hosted-demo QR code works, or its placeholder has been removed.
- [ ] `uv run python scripts/preflight.py` passes.
- [ ] `uv run python scripts/warmup.py` completes.
- [ ] `uv run pytest` passes.
- [ ] Streamlit opens and all nine experiments have been loaded once.
- [ ] The Atlas answer returns 17 November 2026 and AUD 42,000.
- [ ] The carpet question produces an insufficient-evidence response.
- [ ] Offline mode works without `GROQ_API_KEY`.
- [ ] The MCP terminal client creates a local ticket draft.
- [ ] A spare port and a local copy of all files are available.
