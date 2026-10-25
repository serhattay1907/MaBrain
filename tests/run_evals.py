"""
MabrAIn — Eval Runner
Usage: python tests/run_evals.py
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / "backend" / ".env")

from obsidian.router import classify_intent


def run_router_eval():
    eval_file = Path(__file__).parent / "evals" / "router_eval.json"
    cases = json.loads(eval_file.read_text())

    passed, failed, results = 0, 0, []

    for case in cases:
        agent_key, domain = classify_intent(case["input"])
        ok = agent_key == case["expected_agent"]
        passed += ok
        failed += not ok
        results.append({"input": case["input"], "expected": case["expected_agent"], "got": agent_key, "pass": ok})

    total = passed + failed
    accuracy = passed / total * 100

    print(f"\nRouter Eval: {passed}/{total} passed ({accuracy:.1f}%)")
    print("=" * 60)
    for r in results:
        status = "✅" if r["pass"] else "❌"
        print(f"{status} [{r['expected']:12} → {str(r['got']):12}] {r['input'][:50]}")

    target_met = accuracy >= 85
    icon = "🎯" if target_met else "⚠️ "
    print(f"\n{icon} Hedef: ≥85% — Mevcut: {accuracy:.1f}%")
    return accuracy


if __name__ == "__main__":
    run_router_eval()
