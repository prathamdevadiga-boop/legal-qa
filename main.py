import os
import requests
from logger import log_query
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Legal Q&A API", description="RAG-based Indian court case search", version="2.0")
templates = Jinja2Templates(directory="templates")

# clients
es = Elasticsearch("http://localhost:9200")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
IK_TOKEN = os.environ.get("INDIANKANOON_API_TOKEN")
INDEX_NAME = "legal_docs"

def ensure_index():
    try:
        if not es.indices.exists(index=INDEX_NAME):
            es.indices.create(index=INDEX_NAME, mappings={
                "properties": {
                    "title": {"type": "text"},
                    "content": {"type": "text"},
                    "doc_id": {"type": "keyword"},
                    "court": {"type": "keyword"},
                    "date": {"type": "keyword"}
                }
            })
    except Exception as e:
        print(f"Index setup error: {e}")

@app.on_event("startup")
async def startup():
    ensure_index()

class Question(BaseModel):
    question: str

def fetch_from_indiankanoon(query):
    headers = {"Authorization": f"Token {IK_TOKEN}"}
    search_url = f"https://api.indiankanoon.org/search/?formInput={query}&pagenum=0"
    r = requests.post(search_url, headers=headers)
    if r.status_code != 200:
        return []
    data = r.json()
    docs = []
    for doc in data.get("docs", [])[:3]:
        tid = doc.get("tid", "")
        doc_url = f"https://api.indiankanoon.org/doc/{tid}/"
        doc_r = requests.post(doc_url, headers=headers)
        if doc_r.status_code == 200:
            doc_data = doc_r.json()
            raw_html = doc_data.get("doc", "")
            clean_text = BeautifulSoup(raw_html, "html.parser").get_text()[:3000]
            docs.append({
                "title": doc.get("title", "Unknown"),
                "content": clean_text,
                "doc_id": str(tid),
                "court": doc.get("docsource", ""),
                "date": doc.get("publishdate", "")
            })
    return docs
def index_docs(docs):
    for doc in docs:
        es.index(index=INDEX_NAME, id=doc["doc_id"], document=doc)

def search_es(query, top_k=3):
    result = es.search(index=INDEX_NAME, query={
        "multi_match": {
            "query": query,
            "fields": ["title", "content"]
        }
    }, size=top_k)
    hits = result["hits"]["hits"]
    return [h["_source"] for h in hits]

def ask_ollama(question, docs):
    context = "\n\n".join([f"Title: {d['title']}\nCourt: {d['court']}\nDate: {d['date']}\n{d['content']}" for d in docs])
    prompt = f"""You are a legal assistant. Based on the Indian court cases below, give a clear and direct answer to the question.

Context:
{context}

Question: {question}

Give a direct answer in 2-3 sentences. Mention the case name if relevant."""
    r = requests.post(f"{OLLAMA_HOST}/api/generate",
        json={"model": "qwen2.5:3b", "prompt": prompt, "stream": False})
    return r.json()["response"]
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/ask")
async def ask(question: Question):
    docs = fetch_from_indiankanoon(question.question)
    if docs:
        index_docs(docs)
    results = search_es(question.question)
    if not results:
        return {"answer": "No relevant documents found.", "sources": []}
    answer = ask_ollama(question.question, results)
    sources = [{"title": d["title"], "court": d["court"], "date": d["date"]} for d in results]
    log_query(question.question, answer, sources)
    return {"answer": answer, "sources": sources}