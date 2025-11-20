RAG Knowledge Engine

A lightweight, modular Retrieval-Augmented Generation (RAG) microservice that ingests text documents, stores them as vector embeddings, and answers questions using semantic search + LLM reasoning.
Built with FastAPI, ChromaDB, and OpenAI embeddings.

This project demonstrates real-world skills in:

AI systems design

Embedding pipelines & vector search

Building scalable decisioning / knowledge infrastructure

Modern Python API development

LLM-backed retrieval logic

Ingestion, chunking, metadata modeling

Building an integrated UI for non-technical users

Ideal for demonstrating full-stack AI engineering capability in Forward Deployed Engineering, ML Platform, and Applied AI roles.

Features
✅ Document Ingestion (Local CLI)

Drop .txt and .md files into any folder

Run a simple ingestion script to chunk and store them

Automatically assigned unique doc_ids

Stored in ChromaDB persistent collections

✅ Vector Store

Uses OpenAI embeddings (text-embedding-3-small)

Uses ChromaDB persistent vector database

Supports multiple indexes (Knowledge Bases)

✅ RAG Query API

/query endpoint takes:

index_name

question

top_k

Performs semantic search

Constructs a context block

Calls an LLM for grounded reasoning

Returns:

The answer

The exact source chunks

Scores + metadata

✅ Human-Friendly Knowledge Base Discovery

GET /indexes → lists available knowledge bases

GET /indexes/{index}/docs → lists document IDs

Enables UI dropdowns and self-discovery without knowing index names

✅ Mini Web UI (HTML/JS)

Select knowledge base

View docs in that index

Ask questions and view:

Answer

Retrieved chunks

Scores

All client-side, no framework required

⚙️ Tech Stack

Python 3.11

FastAPI

Uvicorn

ChromaDB

OpenAI API

HTML + JavaScript UI

Project Structure
rag-knowledge-engine/
│
├── app/
│   ├── main.py           # FastAPI app + routes
│   ├── store.py          # VectorStore + index/doc helpers
│   ├── embeddings.py     # OpenAI embeddings
│   ├── rag_engine.py     # RAG reasoning pipeline
│   └── models.py         # Pydantic models
│
├── ingest/
│   ├── loaders.py        # Load + chunk document files
│   └── ingest_cli.py     # CLI for directory ingestion
│
├── static/
│   └── index.html        # Mini UI for querying knowledge bases
│
├── data/
│   └── indexes/          # ChromaDB persistent collections
│
├── requirements.txt
├── README.md
└── .gitignore

How It Works
1. Embeddings

Documents are split into chunks (~800 chars) and embedded with:

text-embedding-3-small


Each chunk becomes a high-dimensional vector representing semantic meaning.

2. Vector Store

Vectors + metadata are stored in ChromaDB:

doc_id

chunk text

collection name = knowledge base

Collections persist to data/indexes/.

3. RAG Query Pipeline

A query triggers:

Embed question

Similarity search (top_k)

Format chunks as context

Feed context + question into an LLM

Return grounded answer + source chunks

No hallucinations. No ungrounded answers.

Local Setup
1. Clone and enter the project
git clone https://github.com/<your-username>/rag-knowledge-engine.git
cd rag-knowledge-engine

2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Add your OpenAI key

Create a .env file:

OPENAI_API_KEY=your_key_here

Running the API
Start FastAPI server
uvicorn app.main:app --reload

Open the UI

Your project includes a built-in UI.

Open:

http://127.0.0.1:8000/

API docs:

FastAPI auto-docs are at:

http://127.0.0.1:8000/docs

Ingesting Documents

To ingest local .txt or .md files:

1. Create a folder:
mkdir -p data/raw/my_notes

2. Add .txt or .md files inside it
3. Run ingestion CLI:
python -m ingest.ingest_cli --index my_notes --path data/raw/my_notes


This will:

Load files

Chunk text

Embed chunks

Store them in ChromaDB

Create the index if it doesn't exist

Query Example
POST /query
{
  "index_name": "my_notes",
  "question": "What does Taktile do?",
  "top_k": 3
}


Returns:

answer

sources with doc_ids, scores, and chunk text

Why This Project Matters

This project demonstrates an understanding of:

Retrieval-Augmented Generation

Vector databases

Document chunking strategies

LLM reasoning grounded in retrieval

API design and data models

Production-friendly Python structure

Full-stack thinking (UI + backend + ingestion)

This is exactly the type of work done by:

Forward Deployed Engineers

AI Platform Engineers

ML Engineers

Applied AI / Infra engineers

Decisioning platform implementers

It’s also extensible into:

Multi-index search

Authentication

Ingestion via UI

Agentic querying

Model switching

Document viewers

PDF ingestion

Full UX dashboard