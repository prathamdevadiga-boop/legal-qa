u understood me wrong
markdown

```markdown
# Legal Q&A — RAG-based Indian Court Case Search

Ask natural language questions about real Indian court cases and get accurate answers instantly.

Built with FAISS, Ollama, sentence-transformers and Flask.

## Demo
- Ask "Who is the petitioner in the Kerala High Court case?"
- Ask "What did the court direct the bank to do?"
- Ask "What was the defamation case about?"

## How it works
1. Indian court documents are loaded from the `docs/` folder
2. Text is chunked into 200-word pieces with overlap
3. Each chunk is embedded using `all-MiniLM-L6-v2`
4. Embeddings are stored in a FAISS vector index
5. On each query, top-3 relevant chunks are retrieved
6. Chunks are passed as context to Qwen2.5:3b running locally via Ollama
7. Flask serves a dark-themed web UI with suggestion chips

## Tech stack
- `sentence-transformers` — text embeddings
- `faiss-cpu` — vector similarity search
- `ollama` — local LLM inference (100% offline, no API key needed)
- `flask` — web interface

## Cases loaded
- Cybercrime defamation case — Bengaluru
- Kerala High Court bank account freeze case (2026)
- Cyber fraud case

## Setup

Install dependencies:
```

pip install sentence-transformers faiss-cpu requests flask

```

Pull the LLM:
```

ollama pull qwen2.5:3b

```

Add court documents as .txt files inside docs/ folder.

Build the index:
```

python chatbot.py

```

Start the web app:
```

python app.py

```

Open http://localhost:5000
```
