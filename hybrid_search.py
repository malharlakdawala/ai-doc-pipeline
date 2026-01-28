"""Hybrid search combining keyword and semantic retrieval."""

import re
from retriever import Retriever


class HybridSearcher:
    def __init__(self, retriever: Retriever, keyword_weight: float = 0.3):
        self.retriever = retriever
        self.keyword_weight = keyword_weight

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        # Semantic search
        semantic_results = self.retriever.retrieve(query, top_k=top_k * 2)

        # Keyword matching boost
        query_terms = set(re.findall(r"\w{3,}", query.lower()))

        for result in semantic_results:
            text_lower = result["text"].lower()
            keyword_hits = sum(1 for term in query_terms if term in text_lower)
            keyword_score = min(keyword_hits / max(len(query_terms), 1), 1.0)

            # Blend scores (lower distance = better for semantic)
            semantic_score = 1 - result["distance"]
            result["hybrid_score"] = (
                (1 - self.keyword_weight) * semantic_score
                + self.keyword_weight * keyword_score
            )

        semantic_results.sort(key=lambda r: r["hybrid_score"], reverse=True)
        return semantic_results[:top_k]
