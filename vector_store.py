"""ChromaDB vector store wrapper."""

import chromadb
from chromadb.config import Settings
from config import Config


class VectorStore:
    def __init__(self, collection_name: str = "documents"):
        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: list, embeddings: list[list[float]]):
        ids = [f"chunk_{c.metadata.get('source', 'unknown')}_{c.chunk_index}" for c in chunks]
        documents = [c.text for c in chunks]
        metadatas = [c.metadata for c in chunks]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def query(self, query_embedding: list[float], top_k: int | None = None) -> dict:
        top_k = top_k or Config.TOP_K
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        return results

    def count(self) -> int:
        return self.collection.count()

    def reset(self):
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"},
        )
