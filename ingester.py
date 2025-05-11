"""Document ingestion and parsing module."""

import os
from pathlib import Path
from pypdf import PdfReader
from typing import Generator


class Document:
    def __init__(self, content: str, metadata: dict):
        self.content = content
        self.metadata = metadata

    def __repr__(self):
        return f"Document(source={self.metadata.get('source', 'unknown')}, len={len(self.content)})"


class Ingester:
    SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}

    def __init__(self):
        self._parsers = {
            ".pdf": self._parse_pdf,
            ".txt": self._parse_text,
            ".md": self._parse_text,
        }

    def ingest_directory(self, directory: str) -> list[Document]:
        docs = []
        for path in Path(directory).rglob("*"):
            if path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                docs.extend(self.ingest_file(str(path)))
        return docs

    def ingest_file(self, file_path: str) -> list[Document]:
        ext = Path(file_path).suffix.lower()
        parser = self._parsers.get(ext)
        if not parser:
            raise ValueError(f"Unsupported file type: {ext}")
        return parser(file_path)

    def _parse_pdf(self, file_path: str) -> list[Document]:
        reader = PdfReader(file_path)
        docs = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                docs.append(Document(
                    content=text,
                    metadata={"source": file_path, "page": i + 1}
                ))
        return docs

    def _parse_text(self, file_path: str) -> list[Document]:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return [Document(content=content, metadata={"source": file_path})]
