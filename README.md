# M1_EKA_Gorthi — TechNova Enterprise Knowledge Assistant

## Submission scope

This repository implements the M1/W5 foundation for an Enterprise Knowledge Assistant (EKA). The attached capstone brief defines M1 as the foundation for a future RAG system, with the EKA answering employee questions from approved internal organisational documents, returning citations/confidence, and escalating when information is unavailable.

The M1 implementation intentionally does **not** pretend to be a production RAG system. The FastAPI endpoint is a tested placeholder; the evaluation harness provides the required fake baseline. Real retrieval is the next phase.

## Repository

```text
M1_EKA_Gorthi/
├── docs/
│   ├── adr/
│   │   ├── 0001-capstone-framing.md
│   │   └── 0002-api-contract.md
│   └── stakeholder-map.md
├── src/
│   ├── api/main.py
│   ├── auth/auth.py
│   ├── middleware/middleware.py
│   └── pipeline/models.py
├── data/
│   ├── knowledge_corpus/        # 15 synthetic internal documents
│   ├── golden_set_full.jsonl    # 20 questions: 8/8/4
│   └── GOLDEN_SET_HUMAN_VERIFICATION.md
├── scripts/run_rag_eval.py
├── tests/test_api.py
├── DR1_OnePager.pdf
├── requirements.txt
└── README.md
```

## Corpus design

There are 15 documents, organised into three major topics with 5 documents each:

1. **HR & Workplace** — handbook, leave/PTO, remote work, benefits, performance.
2. **IT & Security** — information security, acceptable use, access management, employee onboarding, IT support.
3. **Business Operations & Compliance** — travel/expense, procurement, data privacy, code of conduct, supplier management.

Each document is 500–3000 words.

## Run the service

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

Test:

```bash
curl -X POST http://127.0.0.1:8000/ask   -H "Authorization: Bearer m1-demo-token"   -H "Content-Type: application/json"   -d '{"question":"How many annual PTO days do I receive?"}'
```

## Run unit tests

```bash
pytest -q
```

## Run the required M1 baseline

```bash
python scripts/run_rag_eval.py --fake --label baseline
```

The output is a deliberately fake W5 baseline. It validates the evaluation plumbing and establishes a floor for later RAG runs.

## Human verification

The course guide requires the golden-set ideal answers to be human-written/human-verified. Before final submission, review every entry against the corpus and complete `data/GOLDEN_SET_HUMAN_VERIFICATION.md`.

## Next phase

Replace the placeholder `/ask` handler with:
1. document loading and metadata,
2. chunking,
3. embeddings,
4. vector retrieval,
5. grounded generation,
6. citation selection,
7. confidence calibration,
8. evaluation against the locked golden set,
9. escalation for unsupported questions.
