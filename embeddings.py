"""Embedding generation using sentence-transformers."""

import logging
from sentence_transformers import SentenceTransformer
from config import settings

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.embedding_model
        self._model = None
        self._dimension = None

    @property
    def model(self):
        if self._model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            self._dimension = self._model.get_sentence_embedding_dimension()
            logger.info(f"Embedding dimension: {self._dimension}")
        return self._model

    @property
    def dimension(self) -> int:
        if self._dimension is None:
            _ = self.model
        return self._dimension

    def generate(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
        return embeddings.tolist()

    def generate_single(self, text: str) -> list[float]:
        embedding = self.model.encode([text], normalize_embeddings=True)
        return embedding[0].tolist()
