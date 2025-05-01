# ai-doc-pipeline

RAG pipeline for document ingestion and AI-powered question answering.

## Features
- PDF and text document ingestion
- Configurable chunking strategies (fixed-size, sentence-based)
- ChromaDB vector store for embeddings
- Claude-powered answer generation with source citations

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
```

## Usage

```bash
# Ingest documents
python main.py ingest ./documents/

# Ask questions
python main.py query "What are the key findings?"

# Interactive mode
python main.py chat
```

## Architecture

```
main.py          -> CLI entry point
ingester.py      -> Document parsing and chunking
embeddings.py    -> Embedding generation
vector_store.py  -> ChromaDB wrapper
retriever.py     -> Similarity search
generator.py     -> Claude answer generation
config.py        -> Settings
```
