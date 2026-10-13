# Architecture and teaching decisions

## Goal

The system makes normally hidden AI infrastructure visible. It is intentionally small enough for students to inspect every chunk, vector score, prompt, citation, resource, and tool argument.

## Data flow

```text
PDF/TXT/Markdown
        |
        v
parse pages -> chunk + metadata -> embed -> searchable matrix
                                           |
question -> embed/keyword search -----------+
        |
        v
ranked evidence -> grounded prompt -> LLM or offline evidence view
        |
        v
condition met -> MCP tool schema -> human approval -> external API boundary
```

## Key decisions

### NumPy search instead of a vector database

The corpus is deliberately small, so normalized vectors and a matrix multiplication are enough. This reveals cosine similarity directly and avoids hiding the first-principles lesson behind infrastructure. A production extension can replace this layer with FAISS, pgvector, Pinecone, or another index.

### TF-IDF plus embeddings

Students can compare exact lexical evidence with semantic similarity. Hybrid retrieval combines both and illustrates why production search rarely relies on one signal.

### PCA for the two-dimensional map

The map is explanatory, not a claim that language is intrinsically two-dimensional. PCA is deterministic, fast, and easier to reproduce than a stochastic projection. Node size shows corpus frequency; positions come from projected term embeddings; edges require either semantic similarity or co-occurrence.

### Offline-first generation

Without a Groq key, the application displays retrieved evidence and citations. With a key, it asks a hosted model to synthesise an answer. Retrieval, mapping, failure experiments, and MCP continue working either way.

### Safe MCP tool

The MCP server exposes two read-only resources and one state-changing tool. The tool writes only a local draft and labels it as requiring human approval. This demonstrates tool boundaries without creating external side effects.

## Production gaps to discuss

The workshop is not a production reference implementation. A production system would also need:

- Durable vector storage and incremental indexing.
- Document-level permissions and tenant isolation.
- OCR and richer parsing.
- Query rewriting, reranking, and hybrid-search tuning.
- Evaluation datasets and continuous regression checks.
- Prompt-injection defences and content filtering.
- Observability, cost controls, retries, and provider fallbacks.
- Tool authorization, audit logs, idempotency, and approval policies.
