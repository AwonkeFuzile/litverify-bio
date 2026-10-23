from pydantic import BaseModel, Field


class AssaySpec(BaseModel):
    """The values we want to pull out of an assay SOP."""

    target_gene: str = Field(description="Gene symbol the assay targets, e.g. EGFR")
    forward_primer: str = Field(description="Forward primer, 5' to 3', letters A, C, G, T only")
    reverse_primer: str = Field(description="Reverse primer, 5' to 3', letters A, C, G, T only")
    annealing_temp_c: float = Field(description="PCR annealing temperature in degrees Celsius")
    source_quote: str = Field(description="The exact sentence copied from the SOP that supports these values")