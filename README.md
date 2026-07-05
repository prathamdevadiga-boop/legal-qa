# Legal Document Q&A

A RAG-based legal document Q&A tool. Ask natural language questions about court cases and get accurate answers.

## How it works
1. Court documents are loaded from the `docs/` folder
2. Text is chunked and embedded using `all-MiniLM-L6-v2`
3. Embeddings are stored in a FAISS vector index
4. Relevant chunks are retrieved and passed to a local LLM (Qwen2.5:3b via Ollama)
5. Flask serves a clean web UI

## Tech stack
- `sentence-transformers` — text embeddings
- `faiss-cpu` — vector similarity search
- `ollama` — local LLM inference
- `flask` — web interface

## Setup
pip install sentence-transformers faiss-cpu requests flask

ollama pull qwen2.5:3b

Add court documents as .txt files in the docs/ folder, then run:
python chatbot.py (to build index)
python app.py (to start web UI)

Open http://localhost:5000
