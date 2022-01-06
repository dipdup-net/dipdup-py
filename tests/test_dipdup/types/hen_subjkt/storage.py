# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from typing import Dict

from pydantic import BaseModel
from pydantic import Extra


class Invoices(BaseModel):
    class Config:
        extra = Extra.forbid

    invoice: str
    subjkt: str


class HenSubjktStorage(BaseModel):
    class Config:
        extra = Extra.forbid

    entries: Dict[str, bool]
    invoices: Dict[str, Invoices]
    manager: str
    metadata: Dict[str, str]
    registries: Dict[str, str]
    subjkts: Dict[str, bool]
    subjkts_metadata: Dict[str, str]
