from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import faiss, pickle, numpy as np, requests, os

app = Flask(__name__)

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("index.faiss")
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

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
    r = requests.post("http://localhost:11434/api/generate",
        json={"model": "qwen2.5:3b", "prompt": prompt, "stream": False})
    return r.json()["response"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question")
    context = search(question)
    answer = ask_ollama(question, context)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)