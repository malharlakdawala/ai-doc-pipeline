"""Retrieval module for finding relevant document chunks."""

from vector_store import VectorStore
from embeddings import EmbeddingGenerator


class Retriever:
    def __init__(self, vector_store: VectorStore, embedder: EmbeddingGenerator):
        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        query_embedding = self.embedder.generate_single(query)
        results = self.vector_store.query(query_embedding, top_k=top_k)

        contexts = []
        for i in range(len(results["documents"][0])):
            contexts.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })

        return contexts

    def build_context_string(self, contexts: list[dict]) -> str:
        parts = []
        for i, ctx in enumerate(contexts, 1):
            source = ctx["metadata"].get("source", "unknown")
            page = ctx["metadata"].get("page", "")
            page_str = f" (page {page})" if page else ""
            parts.append(f"[Source {i}: {source}{page_str}]\n{ctx['text']}")
        return "\n\n---\n\n".join(parts)
