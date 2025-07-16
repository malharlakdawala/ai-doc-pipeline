"""Tests for document ingester."""

import os
import tempfile
import pytest
from ingester import Ingester, Document


@pytest.fixture
def ingester():
    return Ingester()


@pytest.fixture
def sample_text_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("This is a test document.\nIt has multiple lines.\nFor testing purposes.")
        f.flush()
        yield f.name
    os.unlink(f.name)


def test_parse_text_file(ingester, sample_text_file):
    docs = ingester.ingest_file(sample_text_file)
    assert len(docs) == 1
    assert "test document" in docs[0].content
    assert docs[0].metadata["source"] == sample_text_file


def test_unsupported_file_type(ingester):
    with pytest.raises(ValueError, match="Unsupported file type"):
        ingester.ingest_file("file.docx")


def test_ingest_directory(ingester, tmp_path):
    (tmp_path / "doc1.txt").write_text("First document")
    (tmp_path / "doc2.txt").write_text("Second document")
    (tmp_path / "image.png").write_bytes(b"fake image")

    docs = ingester.ingest_directory(str(tmp_path))
    assert len(docs) == 2
