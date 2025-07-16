"""Tests for text chunker."""

import pytest
from chunker import TextChunker


@pytest.fixture
def chunker():
    return TextChunker(chunk_size=100, chunk_overlap=20)


def test_basic_chunking(chunker):
    text = "word " * 200
    chunks = chunker.chunk_text(text)
    assert len(chunks) > 1
    assert all(len(c.text) <= 110 for c in chunks)


def test_small_text_single_chunk(chunker):
    text = "Short text."
    chunks = chunker.chunk_text(text)
    assert len(chunks) == 1
    assert chunks[0].text == "Short text."


def test_chunk_metadata(chunker):
    text = "word " * 200
    chunks = chunker.chunk_text(text, metadata={"source": "test.txt"})
    assert all(c.metadata["source"] == "test.txt" for c in chunks)
    assert all("chunk_index" in c.metadata for c in chunks)


def test_empty_text(chunker):
    chunks = chunker.chunk_text("")
    assert len(chunks) == 0
