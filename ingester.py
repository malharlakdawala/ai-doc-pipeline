"""Document ingestion and parsing module."""

import os
import csv
import logging
from pathlib import Path
from pypdf import PdfReader

logger = logging.getLogger(__name__)


class Document:
    def __init__(self, content: str, metadata: dict):
        self.content = content
        self.metadata = metadata

    def __repr__(self):
        return f"Document(source={self.metadata.get('source', 'unknown')}, len={len(self.content)})"


class Ingester:
    SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".csv"}

    def __init__(self):
        self._parsers = {
            ".pdf": self._parse_pdf,
            ".txt": self._parse_text,
            ".md": self._parse_text,
            ".csv": self._parse_csv,
        }

    def ingest_directory(self, directory: str) -> list[Document]:
        docs = []
        dir_path = Path(directory)
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        for path in sorted(dir_path.rglob("*")):
            if path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    docs.extend(self.ingest_file(str(path)))
                except Exception as e:
                    logger.warning(f"Failed to parse {path}: {e}")
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
            try:
                text = page.extract_text()
            except Exception as e:
                logger.warning(f"Failed to extract page {i+1} of {file_path}: {e}")
                continue
            if text and text.strip():
                text = text.replace("\x00", "").replace("\ufffd", "")
                docs.append(Document(content=text, metadata={"source": file_path, "page": i + 1}))
        return docs

    def _parse_text(self, file_path: str) -> list[Document]:
        encodings = ["utf-8", "latin-1", "cp1252"]
        for enc in encodings:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    content = f.read()
                return [Document(content=content, metadata={"source": file_path})]
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Could not decode: {file_path}")

    def _parse_csv(self, file_path: str) -> list[Document]:
        docs = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                text = " | ".join(f"{k}: {v}" for k, v in row.items() if v)
                docs.append(Document(content=text, metadata={"source": file_path, "row": i + 1}))
        return docs
