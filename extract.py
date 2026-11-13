from pathlib import Path

from google import genai
from google.genai import types

from schema import AssaySpec
from verifier import check_spec

sop_text = Path("sample_sop.txt").read_text()

prompt = f"""Extract the assay specification from the SOP below.
- Write each primer as letters only (A, C, G, T), without the 5'- or -3' parts.
- For source_quote, copy one sentence exactly as written in the SOP.

SOP:
{sop_text}"""

client = genai.Client()

response = client.models.generate_content(
    model="gemini-4-hydrogen",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=AssaySpec,
    ),
)

spec = AssaySpec.model_validate_json(response.text)
print("Model extracted:")
print(spec.model_dump_json(indent=2))

print("\nVerification:")
results = check_spec(spec, sop_text)
for r in results:
    status = "PASS" if r["passed"] else "FAIL"
    print(f"[{status}] {r['check']}: {r['note']}")
print("Overall:", "VERIFIED" if all(r["passed"] for r in results) else "FLAGGED FOR REVIEW")