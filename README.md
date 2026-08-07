# Legal Q&A

Legal Q&A is a RAG system that answers plain‑English legal questions using live Indian court cases, with source citations. Built with FastAPI, Elasticsearch, and a local LLM (Ollama).

![License](https://img.shields.io/github/license/prathamdevadiga-boop/legal-qa)
![Last commit](https://img.shields.io/github/last-commit/prathamdevadiga-boop/legal-qa)

## Demo

Ask a legal question in plain English → get an answer grounded in real Indian court cases with source citations.

**Example:**

> Q: What are bail conditions in a murder case?
> 
> A: In Manikandan vs State Of Kerala (2013), the Kerala High Court held that bail in murder cases requires the court to consider the nature of the offence, severity of punishment, and likelihood of the accused fleeing. In Shankar @ Gauri Shankar vs State Of Tamil Nadu (1994), the Supreme Court emphasized that bail should not be granted where there is a prima facie case of guilt.
>
> Sources: Kerala High Court · 2013-02-19 | Supreme Court of India · 1994-04-04

![Demo](./assets/demo.gif)

## Features

- Live Indian court case data via **Indian Kanoon API** (4+ crore documents)
- **Elasticsearch** for fast document indexing and keyword search
- **RAG pipeline** — retrieves relevant case chunks, passes to local LLM
- **Source citations** — every answer shows case name, court, and date
- **100% local inference** via Ollama (no OpenAI, no API costs)
- Clean dark theme web UI
- Query logging for auditability (planned)

## How it works

1. User types a legal question in the web UI.
2. Backend fetches relevant court documents from Indian Kanoon API.
3. Documents are cleaned, chunked, and indexed into Elasticsearch.
4. For each query, Elasticsearch retrieves the most relevant chunks.
5. Top chunks are passed as context to Ollama (qwen2.5:3b).
6. LLM generates a plain‑English answer grounded in the retrieved case text.
7. Answer is returned with source citations (case name, court, date).

## Tech Stack

| Layer | Technology |
|------|------------|
| Backend | FastAPI + Uvicorn |
| Search & Indexing | Elasticsearch 8.13 |
| LLM Inference | Ollama (qwen2.5:3b) |
| Legal Data | Indian Kanoon API |
| HTML Parsing | BeautifulSoup4 |
| Containerization | Docker |

## Setup

**Prerequisites:** Python 3.11+, Docker, Ollama

1. Clone the repo and install dependencies:
```bash
git clone https://github.com/prathamdevadiga-boop/legal-qa
cd legal-qa
pip install -r requirements.txt
```

2. Add your Indian Kanoon API token to `.env`:
```env
INDIANKANOON_API_TOKEN=your_token_here
```

3. Start Elasticsearch:
```bash
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  elasticsearch:8.13.0
```

4. Start Ollama and pull the model:
```bash
ollama serve
ollama pull qwen2.5:3b
```

5. Run the FastAPI app:
```bash
uvicorn main:app --reload
```

6. Open `http://localhost:8000`

## Usage

**Web UI:**

- Open `http://localhost:8000`
- Type a legal question (e.g., “What are bail conditions in a murder case?”)
- View the generated answer with source citations.

**API example:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are bail conditions in a murder case?"}'
```

## Configuration

| Variable | Description |
|----------|-------------|
| `INDIANKANOON_API_TOKEN` | Your Indian Kanoon API token |
| `OLLAMA_HOST` | Ollama host (default: `http://localhost:11434`) |
| `ES_HOST` | Elasticsearch host (default: `http://localhost:9200`) |

## Project Structure

```text
legal-qa/
├─ main.py
├─ routes/
├─ rag/
├─ frontend/
├─ docker-compose.yml (planned)
├─ requirements.txt
└─ README.md
```

## Roadmap

- [x] Live Indian Kanoon API integration
- [x] Elasticsearch document indexing
- [x] RAG pipeline with source citations
- [x] Dark theme web UI
- [ ] Structured case summarizer (facts, issues, laws, decision)
- [ ] Docker Compose — single command setup
- [ ] Query logging for auditability
- [ ] Hybrid retrieval (keyword + semantic)
- [ ] Structure‑aware chunking by section/paragraph

## Contributing

Open to contributions. Please open an issue before starting work on a new feature.

## License

MIT License — see [LICENSE](./LICENSE) for details.

## Note

All data is sourced from publicly available Indian court records via Indian Kanoon.  
This is a learning project — not legal advice.
