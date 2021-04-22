# generated by datamodel-codegen:
#   filename:  update_record.json

from __future__ import annotations

from typing import Dict, Optional

from pydantic import BaseModel


class UpdateRecord(BaseModel):
    address: Optional[str]
    data: Dict[str, str]
    name: str
    owner: str
