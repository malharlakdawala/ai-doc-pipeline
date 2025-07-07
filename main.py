"""CLI entry point for ai-doc-pipeline."""

import click
from rich.console import Console
from rich.panel import Panel

from config import Config
from ingester import Ingester
from chunker import TextChunker
from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from retriever import Retriever
from generator import AnswerGenerator

console = Console()


@click.group()
def cli():
    """AI Document Pipeline - Ingest docs and ask questions."""
    pass


@cli.command()
@click.argument("path")
@click.option("--chunk-size", default=1000, help="Chunk size in characters")
@click.option("--overlap", default=200, help="Chunk overlap in characters")
def ingest(path: str, chunk_size: int, overlap: int):
    """Ingest documents from a file or directory."""
    console.print(f"[bold]Ingesting documents from:[/bold] {path}")

    ingester = Ingester()
    chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=overlap)
    embedder = EmbeddingGenerator()
    store = VectorStore()

    docs = ingester.ingest_directory(path) if __import__("os").path.isdir(path) else ingester.ingest_file(path)
    console.print(f"  Parsed {len(docs)} documents")

    chunks = chunker.chunk_documents(docs)
    console.print(f"  Created {len(chunks)} chunks")

    texts = [c.text for c in chunks]
    embeddings = embedder.generate(texts)
    store.add_chunks(chunks, embeddings)

    console.print(f"[green]Done![/green] {store.count()} total chunks in store")


@cli.command()
@click.argument("question")
@click.option("--top-k", default=5, help="Number of relevant chunks to retrieve")
def query(question: str, top_k: int):
    """Ask a question about ingested documents."""
    embedder = EmbeddingGenerator()
    store = VectorStore()
    retriever = Retriever(store, embedder)
    generator = AnswerGenerator()

    contexts = retriever.retrieve(question, top_k=top_k)
    context_str = retriever.build_context_string(contexts)

    console.print(Panel(question, title="Question", border_style="blue"))
    console.print()

    answer = generator.generate(question, context_str)
    console.print(Panel(answer, title="Answer", border_style="green"))


@cli.command()
def chat():
    """Interactive chat mode."""
    embedder = EmbeddingGenerator()
    store = VectorStore()
    retriever = Retriever(store, embedder)
    generator = AnswerGenerator()

    console.print("[bold]Interactive mode[/bold] (type 'quit' to exit)")
    while True:
        question = console.input("\n[bold blue]> [/bold blue]")
        if question.lower() in ("quit", "exit", "q"):
            break

        contexts = retriever.retrieve(question)
        context_str = retriever.build_context_string(contexts)

        console.print()
        for chunk in generator.generate_streaming(question, context_str):
            console.print(chunk, end="")
        console.print()


if __name__ == "__main__":
    cli()
