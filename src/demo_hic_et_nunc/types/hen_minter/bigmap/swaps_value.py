# generated by datamodel-codegen:
#   filename:  swaps_value.json

from __future__ import annotations

from pydantic import BaseModel


class SwapsValue(BaseModel):
    issuer: str
    objkt_amount: str
    objkt_id: str
    xtz_per_objkt: str
