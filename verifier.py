import re

from schema import AssaySpec


def normalise(text: str) -> str:
    """Lowercase the text and squash all spaces and line breaks into single spaces,
    so a line break in the SOP doesn't cause a false mismatch."""
    return re.sub(r"\s+", " ", text).strip().lower()


def check_spec(spec: AssaySpec, sop_text: str) -> list[dict]:
    """Compare what the AI extracted (spec) against the original SOP text.
    Returns a list of checks, each marked passed or failed."""
    results = []

    def add(name: str, passed: bool, note: str) -> None:
        results.append({"check": name, "passed": passed, "note": note})

    sop_clean = normalise(sop_text)

    # 1. The quote the AI says it copied must really appear in the SOP, word for word.
    quote_ok = normalise(spec.source_quote) in sop_clean
    add("quote_in_sop", quote_ok,
        "Quote found in SOP" if quote_ok else "Quote NOT found in SOP (possible hallucination)")

    # 2. Each primer must be real DNA letters, and must appear in the SOP exactly.
    for label, primer in [("forward_primer", spec.forward_primer),
                          ("reverse_primer", spec.reverse_primer)]:
        letters_ok = re.fullmatch(r"[ACGT]+", primer.upper()) is not None
        add(f"{label}_is_dna", letters_ok,
            "Only A, C, G, T" if letters_ok else "Contains characters other than A, C, G, T")
        in_sop = primer.upper() in sop_text.upper()
        add(f"{label}_in_sop", in_sop,
            "Sequence found in SOP" if in_sop else "Sequence NOT found in SOP")

    # 3. The target gene symbol must appear in the SOP as a whole word.
    gene_ok = re.search(rf"\b{re.escape(spec.target_gene)}\b", sop_text, re.IGNORECASE) is not None
    add("gene_in_sop", gene_ok,
        "Gene symbol found in SOP" if gene_ok else "Gene symbol NOT found in SOP")

    # 4. The temperature must match a number that appears in the SOP.
    numbers = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", sop_text)]
    temp_ok = spec.annealing_temp_c in numbers
    add("temp_in_sop", temp_ok,
        "Temperature found in SOP" if temp_ok else "Temperature NOT found in SOP")

    return results