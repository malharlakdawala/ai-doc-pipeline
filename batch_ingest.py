"""Batch document ingestion with progress tracking."""

import os
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn
from ingester import Ingester
from chunker import TextChunker
from embeddings import EmbeddingGenerator
from vector_store import VectorStore


def batch_ingest(directories: list[str], chunk_size: int = 1000, overlap: int = 200):
    ingester = Ingester()
    chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=overlap)
    embedder = EmbeddingGenerator()
    store = VectorStore()

    with Progress(SpinnerColumn(), TextColumn("{task.description}")) as progress:
        for directory in directories:
            task = progress.add_task(f"Processing {directory}...", total=None)
            docs = ingester.ingest_directory(directory)
            chunks = chunker.chunk_documents(docs)

            if chunks:
                texts = [c.text for c in chunks]
                embeddings = embedder.generate(texts)
                store.add_chunks(chunks, embeddings)

            progress.update(task, description=f"Done: {directory} ({len(chunks)} chunks)")

    return store.count()
