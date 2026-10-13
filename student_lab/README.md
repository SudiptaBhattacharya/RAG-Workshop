# Student lab: rebuild RAG in five functions

The teaching dashboard is for exploration. This folder is the small system students actually recreate.

## See the complete pipeline once

Run the readable reference implementation:

```bash
uv run python student_lab/rag_walkthrough.py
```

Ask:

```text
When does Project Atlas launch and what is its budget cap?
```

With no Groq key, the script still retrieves evidence and prints the exact grounded prompt. With a key in `.env`, it also generates the final answer.

## Create your working copy

### macOS or Linux

```bash
cp student_lab/rag_starter.py student_lab/my_rag.py
```

### Windows PowerShell

```powershell
Copy-Item student_lab/rag_starter.py student_lab/my_rag.py
```

Work only in `my_rag.py`. The instructor reveals one corresponding function at a time in the workshop app.

## Milestone 1 — load the document

Implement `load_pages`.

Success criteria:

- It returns two pages for `atlas_memo.txt`.
- Every page has `source`, `page`, and `text`.
- Page numbering begins at 1.

Question to answer: why must page metadata survive if we want citations later?

## Milestone 2 — create chunks

Implement `chunk_pages` with a moving character window.

Success criteria:

- Every chunk has `id`, `source`, `page`, and `text`.
- The next chunk begins `overlap` characters before the previous one ended.
- The loop stops at the end of each page.

Experiment with `size=150, overlap=0`, then `size=500, overlap=100`.

## Milestone 3 — create embeddings

Implement `embed_chunks`.

Success criteria:

- There is one vector per chunk.
- The output shape is `(number_of_chunks, 384)` for MiniLM.
- Vectors are normalized so their dot product is cosine similarity.

Question to answer: why is a vector useful when a question paraphrases the document?

## Milestone 4 — retrieve evidence

Implement `retrieve`.

Success criteria:

- The question is embedded with the same model.
- Every chunk receives a similarity score.
- Results are sorted from highest to lowest.
- `top_k` controls how many chunks are returned.

Print the scores. Do not move on until the best result makes sense to a human.

## Milestone 5 — ground the generation

Implement `build_prompt`, then the Groq call in `generate_answer` if a key is available.

Success criteria:

- The prompt contains the question, retrieved text, and source/page labels.
- It instructs the model to use only the evidence.
- It permits an “I do not know” response.
- Retrieved document text is treated as data, not instructions.

## Final test

Run:

```bash
uv run python student_lab/my_rag.py
```

Try three questions:

1. `What is the Project Atlas budget cap?`
2. `Why does the implementation use overlapping chunks?`
3. `What colour is the Project Atlas office carpet?`

The first two should retrieve supporting evidence. The third should expose the need for an insufficient-evidence rule.

## Extension choices

Choose one, rather than adding everything:

- Preserve PDF page numbers with `pdfplumber`.
- Compare keyword and vector retrieval.
- Add a minimum similarity threshold.
- Display citations in a tiny Streamlit interface.
- Evaluate ten questions with Recall@k.
- Replace the NumPy matrix with FAISS or a vector database.
