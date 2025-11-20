from app.models import QueryRequest
from app.rag_engine import answer_question_stub


def test_answer_question_stub():
    req = QueryRequest(index_name="test_index", question="What is this?", top_k=3)
    resp = answer_question_stub(req)
    assert "placeholder answer" in resp.answer
    assert len(resp.sources) == 1
