import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss, pickle, numpy as np, requests

app = FastAPI(title="Legal Q&A API", description="RAG-based Indian court case search", version="1.0")
templates = Jinja2Templates(directory="templates")
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("index.faiss")
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# Ollama host: defaults to localhost for normal local runs.
# When running inside Docker on Windows/Mac, set OLLAMA_HOST=http://host.docker.internal:11434
# so the container can reach Ollama running on your actual machine.
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

class Question(BaseModel):
    question: str

def search(query, top_k=3):
    vec = model.encode([query]).astype("float32")
    _, indices = index.search(vec, top_k)
    return [chunks[i] for i in indices[0]]

def ask_ollama(question, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"""Answer using ONLY the context below.
If the answer isn't there, say "I don't know."
Context:
{context}
Question: {question}
Answer:"""
    r = requests.post(f"{OLLAMA_HOST}/api/generate",
        json={"model": "qwen2.5:3b", "prompt": prompt, "stream": False})
    return r.json()["response"]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/ask")
async def ask(question: Question):
    context = search(question.question)
    answer = ask_ollama(question.question, context)
    return {"answer": answer}
