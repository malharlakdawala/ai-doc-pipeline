# ai-doc-pipeline

RAG (Retrieval-Augmented Generation) pipeline for document ingestion and AI-powered question answering using Claude.

## Features

- **Document Ingestion** - Parse PDFs, text files, and markdown
- **Smart Chunking** - Sentence-aware text splitting with configurable overlap
- **Vector Storage** - ChromaDB for persistent embedding storage
- **Semantic Search** - Find relevant context using embedding similarity
- **AI Answers** - Claude-powered responses with source citations
- **Interactive Chat** - Conversational interface for document Q&A

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your Anthropic API key to .env
```

## Usage

```bash
# Ingest a directory of documents
python main.py ingest ./documents/

# Ingest a single file
python main.py ingest report.pdf

# Ask a question
python main.py query "What are the key findings from the Q3 report?"

# Interactive chat mode
python main.py chat

# View store statistics
python main.py stats

# Reset the vector store
python main.py reset
```

## Architecture

```
Documents -> Ingester -> Chunker -> Embeddings -> VectorStore
                                                      |
Query -> Embeddings -> VectorStore.query -> Retriever -> Generator -> Answer
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | - | Your Anthropic API key |
| `CHUNK_SIZE` | 1000 | Characters per chunk |
| `CHUNK_OVERLAP` | 200 | Overlap between chunks |
| `MODEL` | claude-sonnet-4-20250514 | Claude model for generation |
| `TOP_K` | 5 | Number of chunks to retrieve |

## Testing

```bash
pytest tests/ -v
```
