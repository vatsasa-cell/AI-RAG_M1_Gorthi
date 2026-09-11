#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_fake(items):
    # M1 baseline: deliberately conservative fake output. It exercises the
    # evaluation plumbing without pretending a real RAG system exists.
    results = []
    for item in items:
        is_hard = item["difficulty"] == "Hard/Edge"
        results.append({
            "id": item["id"],
            "difficulty": item["difficulty"],
            "answer": "M1 FAKE BASELINE: no RAG answer generated.",
            "confidence": 0.0 if is_hard else 0.1,
            "sources": [],
            "expected_answerable": item["answerable"],
            "resolved": False,
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="M1 EKA evaluation harness")
    parser.add_argument("--fake", action="store_true", help="run the W5 fake baseline")
    parser.add_argument("--label", default="baseline")
    parser.add_argument("--golden", default="data/golden_set_full.jsonl")
    args = parser.parse_args()

    if not args.fake:
        parser.error("M1 requires --fake; real RAG evaluation is a later-phase extension.")

    items = load_jsonl(Path(args.golden))
    results = run_fake(items)

    total = len(results)
    answerable = sum(r["expected_answerable"] for r in results)
    hard = sum(not r["expected_answerable"] for r in results)
    resolved = sum(r["resolved"] for r in results)
    answerable_resolution = (resolved / answerable) if answerable else 0.0

    summary = {
        "label": args.label,
        "total_questions": total,
        "answerable_questions": answerable,
        "hard_edge_questions": hard,
        "resolved_questions": resolved,
        "answerable_resolution_rate": answerable_resolution,
        "note": "Fake W5 baseline only; not a measure of real RAG quality."
    }

    output = {"summary": summary, "results": results}
    out = Path("eval_results") / f"{args.label}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"Saved detailed results to {out}")


if __name__ == "__main__":
    main()
