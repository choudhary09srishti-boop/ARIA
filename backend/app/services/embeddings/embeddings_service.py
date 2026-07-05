import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

CHROMA_PATH = Path(__file__).resolve().parents[4] / "chroma_db"

client = chromadb.PersistentClient(path=str(CHROMA_PATH))
model = SentenceTransformer("all-MiniLM-L6-v2")

class EmbeddingsService:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.collection = client.get_or_create_collection(f"user_{user_id}")

    def store(self, text: str, doc_id: str, metadata: dict = {}):
        embedding = model.encode(text).tolist()
        self.collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata]
        )

    def search(self, query: str, n_results: int = 3) -> list:
        embedding = model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results["documents"][0] if results["documents"] else []