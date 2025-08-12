import pandas as pd
import os

# Try to import optional ML dependencies
try:
    from chromadb import PersistentClient
    CHROMADB_AVAILABLE = True
except ImportError:
    print("📝 ChromaDB not available")
    CHROMADB_AVAILABLE = False
    
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("📝 sentence-transformers not available")
    SENTENCE_TRANSFORMERS_AVAILABLE = False

# Initialize ML components only if available
chroma_client = None
chroma_collection = None
embedder = None

if CHROMADB_AVAILABLE and SENTENCE_TRANSFORMERS_AVAILABLE:
    # Connect to existing ChromaDB - handle both local and deployment paths
    chroma_path = os.path.join(os.path.dirname(__file__), "ML Strategy", "chroma_storage_rag")
    if not os.path.exists(chroma_path):
        # Fallback path for deployment
        chroma_path = os.path.join(os.path.dirname(__file__), "chroma_storage_rag")
        
    try:
        chroma_client = PersistentClient(path=chroma_path)
        chroma_collection = chroma_client.get_or_create_collection(name="mitigation_knowledge")
        embedder = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        
        # Optional peek
        print("🔎 Sample entries from ChromaDB:")
        print(chroma_collection.peek(3))
        print("📦 Total embeddings:", chroma_collection.count())
        print("🎆 ML components initialized successfully")
    except Exception as e:
        print(f"⚠️ ChromaDB initialization failed: {e}")
        print("📝 Running in fallback mode without ML components")
        chroma_client = None
        chroma_collection = None
        embedder = None
else:
    print("📝 ML dependencies not available, running in basic mode")

def threat_level_from_code(threat_code):
    mapping = {
        "high": 8,
        "moderate": 6,
        "medium": 4,
        "low": 2
    }
    return mapping.get(threat_code.lower(), 1)
def query_mitigation_action(risk_type, threat_level, description=None):
    risk_type = risk_type.strip().lower()
    threat_level = threat_level.strip().lower()

    # Skip ChromaDB queries if not available
    if chroma_collection is None:
        print("📝 ChromaDB not available, using fallback response")
        fallback_desc = description or f"{risk_type} ({threat_level})"
        return {
            "score": 1,
            "action": (
                f"{fallback_desc.title()} —\n"
                "1. Monitor the area periodically for potential risks.\n"
                "2. Record observations and reassess priority if spread increases."
            )
        }

    # 1️⃣ Try metadata query
    try:
        results = chroma_collection.get(
            where={
                "$and": [
                    {"risk_type": {"$eq": risk_type}},
                    {"threat_level": {"$eq": threat_level}}
                ]
            },
            include=["documents", "metadatas"],

        )
        print("🧪 Metadata Query:", results)

        if results["documents"]:
            return {
                "score": "-",
                "action": results["documents"][0]
            }
    except Exception as e:
        print(f"⚠️ Metadata query failed: {e}")

    # 2️⃣ Fallback: Embedding similarity search
    try:
        query_text = f"{risk_type} | {threat_level}"
        embedding = embedder.encode(query_text).tolist()

        results = chroma_collection.query(
            query_embeddings=[embedding],
            n_results=3,
            include=["documents", "distances"]
        )
        print("🧪 Embedding fallback query:", query_text)
        print("🧪 Fallback Results:", results)

        if results["documents"] and results["documents"][0]:
            return {
                "score": results["distances"][0][0],
                "action": results["documents"][0][0]
            }

    except Exception as e:
        print(f"⚠️ Embedding fallback failed: {e}")

    # 3️⃣ Fallback static response
    fallback_desc = description or f"{risk_type} ({threat_level})"
    return {
        "score": 1,
        "action": (
            f"{fallback_desc.title()} —\n"
            "1. Monitor the area periodically for potential risks.\n"
            "2. Record observations and reassess priority if spread increases."
        )
    }

def normalize_threat_code(threat_code):
    return threat_code.lower().replace("risk", "").strip() + " risk"



def generate_mitigation_report(risks):
    if not risks:
        return pd.DataFrame([])

    report_data = []
    for risk in risks:
        risk_type = risk.get("risk_type", "Unknown")
        threat_code_raw = risk.get("threat_code", "low")
        threat_code = threat_code_raw.strip().lower()


        description = risk.get("description", "")

        mitigation = query_mitigation_action(risk_type, threat_code, description)

        report_data.append({
            "Risk Type": risk_type,
            "Threat Level": threat_code.title(),
            "Threat Score": threat_level_from_code(threat_code),
            "Description": description,
            "Mitigation Action": mitigation.get("action", "No action provided.")
        })

    return pd.DataFrame(report_data)
