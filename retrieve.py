import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to existing ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="abhiwan_website"
)

print("RAG retrieval system ready!")


while True:
    question = input("\nAsk a question (type 'exit' to stop): ")

    if question.lower() == "exit":
        break

    # Convert question into embedding
    question_embedding = model.encode([question]).tolist()

    # Search the vector database
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=3
    )

    print("\n--- Relevant Website Information ---")

    for i, document in enumerate(results["documents"][0], 1):
        print(f"\nResult {i}:")
        print(document[:1500])