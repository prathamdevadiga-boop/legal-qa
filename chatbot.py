import os
import pickle
import numpy as np
import requests
import faiss
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "qwen2.5:3b"
INDEX_FILE = "index.faiss"
CHUNKS_FILE = "chunks.pkl"
DOCS_FOLDER = "docs"

def load_docs(folder):
    texts = []
    for fname in os.listdir(folder):
        if fname.endswith(".txt"):
            with open(os.path.join(folder, fname), "r") as f:
                texts.append(f.read())
    return texts

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def build_index(chunks, model):
    print("Building index...")
    embeddings = model.encode(chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, INDEX_FILE)
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Indexed {len(chunks)} chunks.")
    return index, chunks

def search(query, index, chunks, model, top_k=3):
    query_vec = model.encode([query]).astype("float32")
    _, indices = index.search(query_vec, top_k)
    return [chunks[i] for i in indices[0]]

def ask_ollama(question, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"""Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}
Answer:"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

def main():
    model = SentenceTransformer(MODEL_NAME)

    if os.path.exists(INDEX_FILE) and os.path.exists(CHUNKS_FILE):
        print("Loading existing index...")
        index = faiss.read_index(INDEX_FILE)
        with open(CHUNKS_FILE, "rb") as f:
            chunks = pickle.load(f)
    else:
        docs = load_docs(DOCS_FOLDER)
        all_chunks = []
        for doc in docs:
            all_chunks.extend(chunk_text(doc))
        index, chunks = build_index(all_chunks, model)

    print("\nChatbot ready! Type 'quit' to exit.\n")
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        relevant = search(question, index, chunks, model)
        answer = ask_ollama(question, relevant)
        print(f"Bot: {answer}\n")

if __name__ == "__main__":
    main()