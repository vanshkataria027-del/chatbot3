import os
import chromadb
from sentence_transformers import SentenceTransformer

# -----------------------------
# 1. Read website data
# -----------------------------
with open("data/website.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("Website data loaded.")


# -----------------------------
# 2. Split text into chunks
# -----------------------------
chunk_size = 1000
overlap = 200

chunks = []

start = 0

while start < len(text):
    end = start + chunk_size
    chunk = text[start:end]

    if chunk.strip():
        chunks.append(chunk)

    start += chunk_size - overlap

print("Total chunks:", len(chunks))


# -----------------------------
# 3. Load embedding model
# -----------------------------
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# -----------------------------
# 4. Create ChromaDB
# -----------------------------
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="abhiwan_website"
)


# -----------------------------
# 5. Create embeddings
# -----------------------------
print("Creating embeddings...")

embeddings = model.encode(
    chunks,
    show_progress_bar=True
)

# -----------------------------
# 6. Store in ChromaDB
# -----------------------------
ids = [f"chunk_{i}" for i in range(len(chunks))]

collection.upsert(
    ids=ids,
    documents=chunks,
    embeddings=embeddings.tolist()
)

print("\nDONE!")
print("Chunks stored:", len(chunks))
print("Vector database: chroma_db")