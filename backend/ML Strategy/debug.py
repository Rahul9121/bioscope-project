from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

# Setup
client = PersistentClient(path="./ML Strategy/chroma_storage_rag")
collection = client.get_or_create_collection(name="mitigation_knowledge")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode test query
query = "freshwater | high"
embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[embedding],
    n_results=3,
    include=["documents", "distances"]
)

print("📍 Query:", query)
print("🔍 Fallback Results:", results)
