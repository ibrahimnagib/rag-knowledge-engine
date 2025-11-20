from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from .models import (
    QueryRequest,
    QueryResponse,
    IndexListResponse,
    IndexInfo,
    DocListResponse,
)
from .rag_engine import answer_question
from .store import list_indexes, list_docs_in_index, VectorStore
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from ingest.loaders import simple_chunk_text



app = FastAPI(
    title="RAG Knowledge Engine",
    version="0.1.0",
    description="A reusable RAG microservice for querying named knowledge indexes.",
)

BASE_DIR = Path(__file__).resolve().parents[1]
static_dir = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    index_file = static_dir / "index.html"
    return index_file.read_text(encoding="utf-8")

@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query_knowledge(request: QueryRequest) -> QueryResponse:
    return answer_question(request)

@app.get("/indexes", response_model=IndexListResponse)
def get_indexes() -> IndexListResponse:
    raw_indexes = list_indexes()
    items = [
        IndexInfo(id=i["id"], name=i["name"], metadata=i["metadata"])
        for i in raw_indexes
    ]
    return IndexListResponse(indexes=items)


@app.get("/indexes/{index_name}/docs", response_model=DocListResponse)
def get_index_docs(index_name: str) -> DocListResponse:
    docs = list_docs_in_index(index_name)
    return DocListResponse(index_id=index_name, docs=docs)

@app.post("/ingest/upload")
async def ingest_upload(
    index_name: str = Form(..., description="Index to ingest into"),
    file: UploadFile = File(...),
):
    """
    Ingest a single .txt or .md file into the specified index via file upload.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="File must have a filename.")

    suffix = (file.filename.rsplit(".", 1)[-1] or "").lower()
    if suffix not in {"txt", "md"}:
        raise HTTPException(status_code=400, detail="Only .txt and .md files are supported.")

    raw_bytes = await file.read()
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Could not decode file as UTF-8 text.")

    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="File is empty or contains only whitespace.")

    chunks = simple_chunk_text(text, max_chars=800)
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks produced from this file.")

    # doc_id = filename without extension
    doc_id = file.filename.rsplit(".", 1)[0]

    store = VectorStore(index_name=index_name)
    store.add_texts(doc_id=doc_id, texts=chunks)

    return {
        "status": "ok",
        "index_name": index_name,
        "doc_id": doc_id,
        "chunks_ingested": len(chunks),
    }