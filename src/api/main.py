import logging
from fastapi import Depends, FastAPI
from src.auth.auth import require_bearer_token
from src.middleware.middleware import cost_tracking_middleware, logging_middleware
from src.pipeline.models import Answer, AskRequest

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="TechNova Enterprise Knowledge Assistant", version="0.1.0")

app.middleware("http")(logging_middleware)
app.middleware("http")(cost_tracking_middleware)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=Answer)
def ask(request: AskRequest, _token: str = Depends(require_bearer_token)) -> Answer:
    # M1 placeholder: real retrieval begins in the next phase.
    return Answer(
        content=f"M1 placeholder: received question '{request.question}'. Real RAG retrieval will be connected in the next phase.",
        cost_usd=0.0,
        retries=0,
        confidence=0.0,
        sources=[],
    )
