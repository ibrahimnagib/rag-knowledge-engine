from fastapi import FastAPI
from .models import (
    QueryRequest,
    QueryResponse,
    IndexListResponse,
    IndexInfo,
    DocListResponse,
)
from .rag_engine import answer_question
from .store import list_indexes, list_docs_in_index
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path



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
