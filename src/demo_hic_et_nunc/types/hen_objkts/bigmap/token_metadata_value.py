# generated by datamodel-codegen:
#   filename:  token_metadata_value.json

from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, Extra


class TokenInfo(BaseModel):
    class Config:
        extra = Extra.allow

    __root__: str


class TokenMetadataValue(BaseModel):
    token_id: str
    token_info: Dict[str, TokenInfo]
