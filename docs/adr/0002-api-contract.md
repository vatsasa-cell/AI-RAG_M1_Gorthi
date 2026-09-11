# ADR 0002 — API Contract

- **Status:** Accepted for Milestone 1
- **Date:** 2026-09-07
- **Version:** v1

## Purpose

The `/ask` API is locked early so downstream evaluation, cost reporting, retry handling, and future RAG components can evolve without repeatedly changing the external response shape.

## Endpoint Specification

### `POST /ask`

**Authentication**

```text
Authorization: Bearer <token>
```

**Request**

```json
{
  "question": "How many annual PTO days does a full-time employee receive?"
}
```

The request must contain a non-empty `question` string. The initial contract deliberately keeps the request small; retrieval configuration remains an internal implementation concern.

**Successful response**

```json
{
  "content": "A full-time employee receives 20 days of paid time off per calendar year.",
  "cost_usd": 0.0,
  "retries": 0,
  "confidence": 0.0,
  "sources": [],
  "schema_version": "v1"
}
```

At M1 the handler is a placeholder. Real retrieval is introduced in the next phase.

**HTTP behaviour**

- `200`: valid authenticated request and response.
- `401`: missing or invalid Bearer token.
- `422`: malformed request, including an empty question.
- `500`: unexpected server failure.

## Answer Schema

Every endpoint response uses:

```python
class Answer(BaseModel):
    content: str
    cost_usd: float
    retries: int
    confidence: float
    sources: list[str]
    schema_version: str = "v1"
```

The six fields are intentionally retained even though the M1 handler is a stub: later evaluation reads `confidence` and `sources`, cost tracking reads `cost_usd`, retry logic reports `retries`, and all consumers can identify the schema with `schema_version`.

## Versioning Rules

- Start at `v1`.
- Adding an optional response field is **additive** and remains backward-compatible.
- Changing/removing a required field, changing a field's meaning/type incompatibly, or changing endpoint semantics is **breaking** and requires a new schema version.
- Breaking changes use a new version and a documented migration/parallel-running period.
- Existing clients must continue receiving the previous contract during the migration period when feasible.
- A scope change that affects evaluation semantics must be recorded in a new/superseding ADR.

## Alternatives Considered

### REST vs GraphQL
REST was selected because the M1 use case is a small, stable question-answer endpoint. GraphQL was rejected as unnecessary contract complexity at this stage.

### `/ask` vs separate `/ask/cheap` and `/ask/quality`
A single `/ask` endpoint was selected. Splitting by model/quality would expose implementation choices prematurely and make the contract harder to evolve. Routing and model selection can remain internal.

## Trade-offs and Future Evolution

The contract limits internal freedom because downstream components depend on the six fields. This is intentional: stable interfaces make independent evolution possible.

Future RAG metadata such as `retrieved_chunks` should be introduced additively if it can be optional without changing the meaning of existing fields. A breaking redesign should use a new schema version rather than silently changing v1.

## Decision

Freeze the v1 six-field `Answer` contract for M1 and evolve it through additive changes where possible.
