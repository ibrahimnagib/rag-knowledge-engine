from typing import List
from openai import OpenAI

from .config import config
from .models import QueryRequest, QueryResponse, SourceSnippet
from .store import VectorStore

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        if not config.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")
        _client = OpenAI(api_key=config.openai_api_key)
    return _client


def build_context_snippets(request: QueryRequest) -> List[SourceSnippet]:
    store = VectorStore(index_name=request.index_name)
    results = store.similarity_search(request.question, top_k=request.top_k)

    sources: List[SourceSnippet] = []
    for chunk, score in results:
        sources.append(
            SourceSnippet(
                doc_id=chunk.doc_id,
                snippet=chunk.text,
                score=score,
            )
        )
    return sources


def build_prompt(question: str, sources: List[SourceSnippet]) -> str:
    context_parts = []
    for src in sources:
        context_parts.append(f"[{src.doc_id}] {src.snippet}")
    context_block = "\n\n".join(context_parts)

    prompt = f"""
You answer questions based only on the context below.

Context:
{context_block}

Question: {question}

Instructions:
- Use only the information from Context.
- If the answer is not clearly in the Context, say you don't know based on the provided documents.
- When appropriate, mention which doc_id(s) your answer is based on.
"""
    return prompt.strip()


def answer_question(request: QueryRequest) -> QueryResponse:
    # 1) Retrieve relevant chunks
    sources = build_context_snippets(request)

    if not sources:
        return QueryResponse(
            answer="I don't know based on the documents in this index.",
            sources=[],
        )

    # 2) Build prompt
    prompt = build_prompt(request.question, sources)

    # 3) Call OpenAI
    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # swap to any model you have access to
        messages=[
            {"role": "system", "content": "You are a careful, grounded assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    answer_text = response.choices[0].message.content

    return QueryResponse(
        answer=answer_text,
        sources=sources,
    )
