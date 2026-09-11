from fastapi.testclient import TestClient
from src.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ask_requires_bearer_token():
    response = client.post("/ask", json={"question": "What is the PTO policy?"})
    assert response.status_code == 401


def test_ask_returns_answer_schema():
    response = client.post(
        "/ask",
        headers={"Authorization": "Bearer m1-demo-token"},
        json={"question": "How many PTO days do I receive?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {
        "content", "cost_usd", "retries",
        "confidence", "sources", "schema_version"
    }
    assert body["schema_version"] == "v1"


def test_ask_rejects_empty_question():
    response = client.post(
        "/ask",
        headers={"Authorization": "Bearer m1-demo-token"},
        json={"question": ""},
    )
    assert response.status_code == 422
