# Facilitator runbook

Use this runbook for the two-hour first-principles workshop. The application contains the student-facing demonstrations; this document covers facilitation and recovery.

## Before participants arrive

1. Run `uv sync`.
2. Run `uv run python scripts/preflight.py`.
3. Run `uv run python scripts/warmup.py`.
4. Run `uv run pytest`.
5. Start `uv run streamlit run app.py`.
6. Open `0 · RAG code walkthrough` and run the complete minimal pipeline once.
7. Open every later experiment once to populate caches.
8. In a second terminal, verify `uv run python mcp_demo_client.py`.
9. Confirm offline mode works by temporarily removing `GROQ_API_KEY` from the process.
10. Restore the key if using live generation.

Ask students to create a personal working copy before the session:

```bash
cp student_lab/rag_starter.py student_lab/my_rag.py
```

## Teaching rhythm

For every experiment:

1. State the question without naming the new concept.
2. Ask students to predict the result.
3. Run the smallest possible comparison.
4. Inspect the output before explaining it.
5. Name and explain the concept.
6. Ask what the current system still cannot do.
7. Use that limitation to introduce the next experiment.

## Timed delivery: see it, rebuild it, interrogate it

### 0:00–0:08 — See the whole pipeline

- Open `0 · RAG code walkthrough`.
- Show only the five connecting lines: load, chunk, embed, retrieve, generate.
- Run the complete minimal implementation once.
- Do not explain every line yet. Ask students to describe the data changing at each arrow.

Outcome: students have a complete mental map before meeting individual terms.

### 0:08–0:15 — Establish the need

- Open Experiment 1 and ask about Project Atlas without the memo.
- Reveal the private ground truth.
- Establish: fluent model output is not evidence, and a new document is not stored in model parameters.

Outcome: retrieval is introduced as a response to an observed limitation.

### 0:15–0:23 — Rebuild Step 1: load pages

- Students implement `load_pages` in `student_lab/my_rag.py`.
- Reveal only the `load_pages` function in the app.
- Print the two page dictionaries.
- Ask why source and page metadata must survive from the beginning.

Checkpoint: two pages, numbered from 1, each with source/page/text.

### 0:23–0:35 — Rebuild Step 2: chunk

- Students implement `chunk_pages`.
- Run 150/0 and 500/100 configurations in Experiment 3.
- Find a fact that is weakened by a boundary and restore it with overlap.

Checkpoint: chunk IDs are unique, overlap is visible, and no loop runs past the page end.

### 0:35–0:48 — Rebuild Step 3: embed

- Students implement `embed_chunks`.
- Print the matrix shape rather than all vector values.
- Use Experiment 4 to compare two paraphrases with an unrelated sentence.
- Show the top-30 map only after students understand one cosine comparison.

Checkpoint: one normalized 384-dimensional vector per chunk.

### 0:48–1:01 — Rebuild Step 4: retrieve

- Students implement `retrieve` using one question vector, a matrix multiplication, sorting, and top-k.
- Print every returned score.
- Use Experiment 5 to race exact keyword search against a paraphrased vector query.

Checkpoint: the Atlas budget chunk ranks first for both the direct and paraphrased questions.

### 1:01–1:14 — Rebuild Step 5: ground the answer

- Students implement `build_prompt`.
- Inspect the prompt in offline mode before making any API call.
- If a Groq key is available, add the small chat-completion call.
- Run Experiment 6 and compare the original answer with the retrieved-context answer.

Checkpoint: the prompt contains the question, evidence, citations, and an insufficient-evidence rule.

### 1:14–1:27 — Break the student implementation

- Use Experiment 7 for no overlap, low/high top-k, an unanswerable question, and retrieved prompt injection.
- Students identify whether each failure belongs to parsing, retrieval, generation, data, or security.
- Add one improvement to `my_rag.py`: a score threshold, refusal, or citation check.

Outcome: students learn that building RAG is easy; evaluating retrieval is the real engineering work.

### 1:27–1:38 — Place RAG inside the larger architecture

- Use Experiment 2 briefly to label the Groq call as an API request.
- Use Experiment 8 to contrast an MCP resource with a tool.
- Run Experiment 9 and label the relay: RAG evidence → model decision → MCP tool → API boundary → human approval.

Outcome: API, RAG, and MCP are understood as complementary layers.

### 1:38–1:53 — Make it theirs

- Students replace `atlas_memo.txt` with a short document of their own.
- They ask one answerable and one unanswerable question.
- They adjust chunk size or top-k once and explain the observed change.
- Fast finishers choose one extension from `student_lab/README.md`.

### 1:53–2:00 — Explain-back

In pairs, students explain their own code without using the phrase “AI magic”:

1. What information enters and leaves each of the five functions?
2. Why did their top chunk rank first?
3. What evidence would make the system refuse to answer?
4. Where does an API or MCP tool begin, and what permission should it have?

## Recovery procedures

### Hosted LLM fails

Remove or ignore `GROQ_API_KEY` and continue in offline grounded-demo mode. The learning objective is evidence selection, not provider availability.

### Internet fails

The API experiment displays a local fallback response. Embeddings work if `scripts/warmup.py` was run beforehand. MCP is local.

### A student machine fails

Pair the student with another participant. Do not spend workshop time repairing system Python or corporate proxy settings.

### Retrieval looks wrong

Reset the sidebar to chunk size 500, overlap 100, top-k 4, and hybrid retrieval. Confirm the included sample corpus is selected.

### The model ignores the evidence

Show the retrieved chunks directly and score retrieval separately. Then continue in offline mode to preserve the grounding lesson.

## After the workshop

- Delete or rotate any shared API key.
- Remove `data/output/ticket_draft.json` if it is no longer needed.
- Capture student questions and failed queries as candidates for an evaluation dataset.
- Record the embedding model, Groq model, and dependency lockfile used for the session.
