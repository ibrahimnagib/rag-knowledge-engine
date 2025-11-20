from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any



class QueryRequest(BaseModel):
    index_name: str = Field(..., description="Name of the knowledge index to query")
    question: str = Field(..., description="User's question")
    top_k: int = Field(5, ge=1, le=20, description="Number of chunks to retrieve")


class SourceSnippet(BaseModel):
    doc_id: str
    snippet: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceSnippet]

class IndexInfo(BaseModel):
    id: str
    name: str
    metadata: Dict[str, Any] = {}


class IndexListResponse(BaseModel):
    indexes: List[IndexInfo]


class DocListResponse(BaseModel):
    index_id: str
    docs: List[str]
