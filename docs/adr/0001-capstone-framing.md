# ADR 0001 — Capstone Framing

- **Status:** Accepted for Milestone 1
- **Date:** 2026-09-07
- **Decision owner:** AI Solutions Architect
- **Scope lock:** Milestone 1 / W5

## Context

TechNova Solutions is a fictional organisation used for this capstone. Employees currently depend on HR teams for policy clarification, IT helpdesks for technical procedures, managers for operational guidance, and internal portals that are difficult to search. This creates avoidable waiting time and inconsistent discovery of approved information.

The proposed Enterprise Knowledge Assistant (EKA) is intentionally narrow: it answers employee questions from approved internal organisational documents, provides source references and a confidence indicator, and escalates when the corpus does not contain sufficient evidence.

## Problem Statement

Employees need a faster and more reliable way to locate existing organisational knowledge without replacing policy owners, HR, IT, managers, or formal approval processes. The EKA should retrieve existing content rather than invent new policy or make decisions on behalf of employees.

## EKA Scope

### In scope
- Employee question-and-answer interaction.
- Internal HR, IT/Security, and Business Operations/Compliance knowledge.
- Retrieval from the approved capstone corpus.
- Grounded answers with document citations.
- Confidence indication.
- Honest escalation when evidence is missing or insufficient.
- A stable `/ask` API contract.

### Out of scope
- Public-web question answering.
- Research-paper review.
- Policy creation or policy interpretation beyond corpus evidence.
- Transaction execution or approval.
- Code generation, image generation, or autonomous decision making.
- Replacing HR, IT, Legal, Privacy, Security, Procurement, or managers.

## Stakeholders

The primary users are regular employees who need fast policy/process answers and policy/process specialists who need traceable sources. HR, IT/Security, Procurement/Operations, and programme sponsors are secondary stakeholders because they own or govern the knowledge being retrieved.

## KPI Targets

| KPI | Baseline | Target | Business justification |
|---|---:|---:|---|
| Question resolution rate | 0% automated EKA resolution at M1 | ≥80% of answerable golden questions | Demonstrates useful self-service while leaving edge cases for escalation. |
| Retrieval/source accuracy | 0% measured baseline before retrieval is implemented | ≥90% correct source on answerable evaluation questions | An employee assistant is only trustworthy when it retrieves the right organisational evidence. |
| Employee answer latency | Current process is manual and can require waiting for HR/IT/SME response; no instrumented numeric baseline yet | ≥90% of answered requests within 30 seconds | A fast response is necessary to improve the employee experience and reduce dependency on synchronous support. |

**Measurement note:** The M1 baseline is a design baseline where a numeric operational baseline is not yet available. W6+ instrumentation should replace these placeholders with observed production/pilot measurements.

## Technology Approach

M1 uses a thin FastAPI service contract with Bearer-token authentication, request logging, cost tracking, a Pydantic `Answer` schema, unit tests, and a fake evaluation harness. The next phase will add document ingestion, chunking, embeddings, vector retrieval, grounded generation, citations, confidence calibration, and retrieval evaluation.

High-level target architecture:

`Employee → FastAPI /ask → Auth → Query handling → Retriever → LLM grounded on retrieved chunks → Answer + confidence + sources → Employee`

## Alternatives Considered

### 1. Search-only portal
Rejected as the primary EKA approach because keyword search can return documents but does not provide a concise, grounded question-and-answer experience.

### 2. General-purpose LLM without retrieval
Rejected because it can answer from model knowledge rather than approved organisational documents, creating a higher hallucination and governance risk.

### 3. Public-web / enterprise-wide open-domain assistant
Rejected for M1 because the programme defines the EKA around internal organisational knowledge and employee Q&A. Broadening the source boundary would make citation, governance, and evaluation less controlled.

## Trade-offs

1. **Narrow corpus vs broad coverage:** A controlled internal corpus is easier to evaluate and govern, but it will intentionally fail questions outside scope.
2. **FastAPI REST contract vs internal flexibility:** A stable contract constrains internal implementation, but it allows evaluation, cost tracking, and later retrieval components to evolve independently.
3. **Confidence + escalation vs maximum answer rate:** Some questions will be refused. This reduces apparent coverage but is safer than confidently fabricating policy.

## Risks and Open Questions

- Retrieval quality and chunking strategy are not yet validated.
- Confidence thresholds require empirical calibration.
- The synthetic corpus must be replaced or formally approved if real organisational documents are introduced.
- Production identity, authorization, audit retention, and document-version governance require later design.
- KPI baselines need measurement during pilot operation.

## Decision

Proceed with a scoped employee EKA over the 15-document synthetic TechNova corpus, with a stable API and evaluation foundation now and real RAG retrieval beginning in the next phase.
