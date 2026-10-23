from pathlib import Path

from schema import AssaySpec
from verifier import check_spec

sop_text = Path("sample_sop.txt").read_text()

# Pretend this answer came from an AI model, and it is correct.
good = AssaySpec(
    target_gene="EGFR",
    forward_primer="GCAATATCAGCCTTAGGTGC",
    reverse_primer="GATCCAAAGGTCATCAAGGG",
    annealing_temp_c=58.5,
    source_quote="Thermal cycler setup: anneal at 58.5 degrees Celsius for 30 seconds.",
)

# Pretend this one is a bad AI answer: wrong last letter, wrong temperature, invented quote.
bad = AssaySpec(
    target_gene="EGFR",
    forward_primer="GCAATATCAGCCTTAGGTGC",
    reverse_primer="GATCCAAAGGTCATCAAGGA",
    annealing_temp_c=60.0,
    source_quote="Anneal at 60 degrees Celsius for 45 seconds.",
)


def report(label: str, spec: AssaySpec) -> None:
    print(f"\n=== {label} ===")
    results = check_spec(spec, sop_text)
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"[{status}] {r['check']}: {r['note']}")
    overall = "VERIFIED" if all(r["passed"] for r in results) else "FLAGGED FOR REVIEW"
    print(f"Overall: {overall}")


report("Correct AI answer", good)
report("Bad AI answer", bad)