# litverify-bio
A small learning project: check whether values extracted from a lab protocol (SOP) are really supported by the source text.

AI tools can invent details when they extract data from scientific documents. This project builds the **verification layer**: simple, deterministic checks that compare an extracted assay specification against the original SOP and flag anything that does not match. It is a learning project inspired by published work on schema-guided extraction and verification of LLM output in biology, not a validated tool.

## What it checks

For an extracted PCR assay specification (target gene, forward and reverse primers, annealing temperature, supporting quote):

- the supporting quote appears in the SOP word for word
- each primer contains only A, C, G, T
- each primer sequence appears in the SOP
- the gene symbol appears in the SOP
- the annealing temperature is a number that appears in the SOP

## Files

- `schema.py`: defines the fields to extract (Pydantic)
- `verifier.py`: the checks
- `run_demo.py`: tests the checker with one correct and one deliberately wrong "AI answer"
- `sample_sop.txt`: an **invented** SOP used for testing, not a real validated assay

## Run it

    pip install pydantic biopython
    python run_demo.py

## Example output (deliberately wrong answer)

    [FAIL] quote_in_sop: Quote NOT found in SOP (possible hallucination)
    [PASS] forward_primer_is_dna: Only A, C, G, T
    [PASS] forward_primer_in_sop: Sequence found in SOP
    [PASS] reverse_primer_is_dna: Only A, C, G, T
    [FAIL] reverse_primer_in_sop: Sequence NOT found in SOP
    [PASS] gene_in_sop: Gene symbol found in SOP
    [FAIL] temp_in_sop: Temperature NOT found in SOP
    Overall: FLAGGED FOR REVIEW

## Known limitations

- The temperature check only tests that the number appears somewhere in the SOP. A wrong number that happens to appear elsewhere (for example, 30 seconds reported as 30 degrees) would pass. A stronger check would look for the number next to the word "anneal".
- The gene check does not yet verify the symbol against a database (NCBI) or the organism.
- Only one made-up SOP is tested so far. The "AI answers" in the demo are written by hand; no language model is connected yet.

## Next steps

- Connect a language model to produce the extraction automatically
- Test on more varied SOP text and record where the checker fails
- Add a database check for gene symbols
