**RAG Knowledge Engine**
========================

A lightweight, modular **Retrieval-Augmented Generation (RAG) microservice** that ingests text documents, stores them as vector embeddings, and answers questions using semantic search + LLM reasoning.\
Built with **FastAPI**, **ChromaDB**, and **OpenAI embeddings**, and deployed on **Render**.

**Live Demo:**\
**<https://rag-knowledge-engine.onrender.com>**

This project demonstrates real-world skills in:

-   AI systems design

-   Vector search architecture

-   Embedding pipelines + text chunking

-   LLM-backed retrieval

-   Modern API development with FastAPI

-   Front-end integration for interactive querying

-   Deployment of AI infra to production

Suitable for roles in Forward Deployed Engineering, AI Platform, ML Infrastructure, Applied AI, and Decisioning Systems.

* * * * *

**Features**
------------

### **Document Ingestion (CLI)**

-   Add `.txt` or `.md` documents to your knowledge base

-   Automatic chunking + embedding

-   Indexes stored in persistent ChromaDB collections

### **Vector Database**

-   Uses **ChromaDB** for high-performance vector search

-   Each index is a separate collection (knowledge base)

-   Metadata support for doc IDs, display names, etc.

### **RAG Pipeline**

-   Query any knowledge base using semantic search

-   Retrieves most relevant chunks (top_k)

-   Constructs grounded context

-   Calls an LLM for an accurate, source-grounded answer

-   Returns chunks + scores for transparency

### **Interactive UI (No Framework Required)**

Available at the root URL:

**<https://rag-knowledge-engine.onrender.com>**

Includes:

-   Knowledge base selector

-   Document listing

-   RAG query box

-   Answer viewer

-   Source viewer with doc IDs + similarity scores

### **REST API Endpoints**

`GET  /health                        → health check
GET  /indexes                       → list knowledge bases
GET  /indexes/{index}/docs          → list docs in an index
POST /query                         → run RAG query`

* * * * *

**Project Structure**
---------------------

`rag-knowledge-engine/
│
├── app/
│   ├── main.py           # FastAPI app + routes
│   ├── store.py          # VectorStore + index/doc helpers
│   ├── embeddings.py     # OpenAI embedding logic
│   ├── rag_engine.py     # Retrieval-augmented generation pipeline
│   └── models.py         # Pydantic models for requests/responses
│
├── ingest/
│   ├── loaders.py        # Load + chunk .txt and .md files
│   └── ingest_cli.py     # CLI tool for ingestion
│
├── static/
│   └── index.html        # Browser UI for interactive querying
│
├── data/
│   └── indexes/          # Chroma persistent DB (ignored in Git)
│
├── requirements.txt
├── runtime.txt
├── README.md
└── .gitignore`

* * * * *

**How It Works**
================

### **1\. Chunking + Embeddings**

-   Documents split into ~800-character chunks

-   Embedded using `text-embedding-3-small`

-   Stored with metadata: `doc_id`, text, vector

### **2\. Vector Search**

-   All chunks stored in ChromaDB collection

-   Query embedding compared to stored vectors

-   Top-K chunks returned by cosine similarity

### **3\. RAG Answering**

Pipeline:

1.  Embed user query

2.  Retrieve chunks

3.  Construct contextual prompt

4.  Call LLM (e.g., GPT-4o-mini)

5.  Return grounded answer + sources

No hallucinations --- answers are limited to retrieved context.

* * * * *

**Local Setup**
===============

### Clone and enter the project

`git clone https://github.com/<your-username>/rag-knowledge-engine.git
cd rag-knowledge-engine`

### Create virtual environment

`python3 -m venv venv
source venv/bin/activate`

### Install dependencies

`pip install -r requirements.txt`

### Add environment variable

Create `.env`:

`OPENAI_API_KEY=your_openai_key`

* * * * *

**Running Locally**
===================

Start the API:

`uvicorn app.main:app --reload`

Open:

-   UI:\
    **http://127.0.0.1:8000/**

-   API docs:\
    **http://127.0.0.1:8000/docs**

* * * * *

**Ingesting Documents**
=======================

Add `.txt` or `.md` files:

`mkdir -p data/raw/job_prep`

Drop your files into that folder.

Run ingestion:

`python -m ingest.ingest_cli --index job_prep --path data/raw/job_prep`

This will:

-   Load the files

-   Chunk them

-   Embed chunks

-   Store them in the `job_prep` knowledge base

* * * * *

**Query Example**
=================

POST `/query`:

`{
  "index_name": "job_prep",
  "question": "What does Taktile do?",
  "top_k": 3
}`

Response:

-   `answer` --- LLM-generated summary grounded in sources

-   `sources` --- list of chunks, doc_ids, and similarity scores

* * * * *

**Deployment**
==============

### Hosted on Render:

**<https://rag-knowledge-engine.onrender.com>**

Render config:

-   **Build Command:**\
    `pip install -r requirements.txt`

-   **Start Command:**\
    `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

-   **Environment Vars:**\
    `OPENAI_API_KEY=your_key_here`

* * * * *

**Roadmap**
===========

-   File-upload ingestion from UI

-   Multi-index search

-   Chat-style interface

-   PDF ingestion

-   Middleware for per-index authorization

-   Docker support

-   Usage logging + analytics dashboard

* * * * *

**Why This Project Matters**
============================

This codebase shows practical experience with:

-   Retrieval-Augmented Generation

-   Vector databases

-   LLM inference pipelines

-   Backend API design

-   Semantic search

-   Embedding modeling

-   Front-end + backend integration

-   Cloud deployment of AI systems

These are core patterns in modern AI engineering and decisioning platforms.