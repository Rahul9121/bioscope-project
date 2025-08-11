import pandas as pd
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

# Load your CSV (keep original formatting in column values)
df = pd.read_csv("data sources/mitigation_action_cleaned.csv")

# Setup ChromaDB client and collection
client = PersistentClient(path="./chroma_storage_rag")
collection = client.get_or_create_collection(name="mitigation_knowledge")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Clear existing documents safely
existing_ids = collection.get()["ids"]
if existing_ids:
    collection.delete(ids=existing_ids)

# Embed and add data using unaltered 'risk_type' and 'threat_level'
for idx, row in df.iterrows():
    risk_type = str(row.get("risk_type", "")).strip()                # e.g., "Invasive Species"
    threat_level = str(row.get("threat_level", "")).strip().title()  # e.g., "High"
    action = str(row.get("mitigation_action", "")).strip()

    if not risk_type or not threat_level or not action:
        continue  # Skip incomplete entries

    query_text = f"{risk_type} | {threat_level}"
    embedding = model.encode(query_text).tolist()

    collection.add(
        documents=[action],
        metadatas=[{
            "risk_type": risk_type,
            "threat_level": threat_level,
        }],
        ids=[f"mitigation-{idx}"],
        embeddings=[embedding]
    )

# Show a few entries to confirm
print("✅ Embedding complete.")
print("Total documents stored:", collection.count())
print("Preview:")
print(collection.peek(3))
