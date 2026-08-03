# Legal Q&A

A RAG-based (Retrieval-Augmented Generation) Q&A system for Indian legal/court documents. Ask a question, and it retrieves the most relevant chunks from the loaded case documents and uses a local LLM to generate an answer grounded in that context.

## How it works

1. Court case documents are pre-processed and embedded using `sentence-transformers` (`all-MiniLM-L6-v2`)
2. Embeddings are stored and searched using **FAISS** for fast similarity search
3. On a question, the top matching chunks are retrieved and passed as context to **Ollama** (running `qwen2.5:3b` locally) to generate a grounded answer
4. Served via a **FastAPI** backend with a simple web UI

## Tech stack

- FastAPI + Uvicorn
- FAISS (vector search)
- sentence-transformers
- Ollama (local LLM inference)
- Docker

## Running locally (without Docker)

**Prerequisites:** Python 3.11, Ollama installed and running with the `qwen2.5:3b` model pulled (`ollama pull qwen2.5:3b`).

\`\`\`
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
\`\`\`

Then open `http://localhost:8000`

## Running with Docker

**Prerequisite:** Ollama running on your host machine with `qwen2.5:3b` pulled.

\`\`\`
docker build -t legal-qa .
docker run -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 legal-qa
\`\`\`

Then open `http://localhost:8000`

> Note: `OLLAMA_HOST` is set to `host.docker.internal` because inside a Docker container, `localhost` refers to the container itself, not your host machine where Ollama is running.

## Status / Roadmap

- [x] RAG pipeline with FAISS + sentence-transformers
- [x] FastAPI backend
- [x] Dockerized deployment
- [ ] Court Case Summarizer feature
- [ ] Source citations in answers
