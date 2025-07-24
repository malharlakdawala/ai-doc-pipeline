"""Text chunking strategies for document processing."""

from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    metadata: dict
    chunk_index: int


class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, metadata: dict | None = None) -> list[Chunk]:
        if not text or not text.strip():
            return []

        metadata = metadata or {}
        chunks = []
        start = 0
        chunk_idx = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                for sep in [". ", "\n\n", "\n", " "]:
                    last_sep = text.rfind(sep, start + self.chunk_size // 3, end)
                    if last_sep > start:
                        end = last_sep + len(sep)
                        break

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(Chunk(
                    text=chunk_text,
                    metadata={**metadata, "chunk_index": chunk_idx},
                    chunk_index=chunk_idx,
                ))
                chunk_idx += 1

            next_start = end - self.chunk_overlap
            if next_start <= start:
                next_start = end
            start = next_start

        return chunks

    def chunk_documents(self, documents: list) -> list[Chunk]:
        all_chunks = []
        for doc in documents:
            chunks = self.chunk_text(doc.content, doc.metadata)
            all_chunks.extend(chunks)
        return all_chunks
