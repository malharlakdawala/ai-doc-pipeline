"""Embedding generation using sentence-transformers."""

from sentence_transformers import SentenceTransformer
from config import Config


class EmbeddingGenerator:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or Config.EMBEDDING_MODEL
        self._model = None

    @property
    def model(self):
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def generate(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()

    def generate_single(self, text: str) -> list[float]:
        embedding = self.model.encode([text])
        return embedding[0].tolist()
