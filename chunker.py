"""Text chunking strategies for document processing."""

from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    metadata: dict
    chunk_index: int


class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, metadata: dict | None = None) -> list[Chunk]:
        metadata = metadata or {}
        chunks = []
        start = 0
        chunk_idx = 0

        while start < len(text):
            end = start + self.chunk_size

            # Try to break at sentence boundary
            if end < len(text):
                last_period = text.rfind(".", start, end)
                last_newline = text.rfind("\n", start, end)
                break_point = max(last_period, last_newline)
                if break_point > start + self.chunk_size // 2:
                    end = break_point + 1

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(Chunk(
                    text=chunk_text,
                    metadata={**metadata, "chunk_index": chunk_idx},
                    chunk_index=chunk_idx,
                ))
                chunk_idx += 1

            start = end - self.chunk_overlap
            if start >= len(text):
                break

        return chunks

    def chunk_documents(self, documents: list) -> list[Chunk]:
        all_chunks = []
        for doc in documents:
            chunks = self.chunk_text(doc.content, doc.metadata)
            all_chunks.extend(chunks)
        return all_chunks
