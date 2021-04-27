# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from typing import Any, Dict, List, Union

from pydantic import BaseModel


class Key(BaseModel):
    address: str
    nat: str


class LedgerItem(BaseModel):
    key: Key
    value: str


class Key1(BaseModel):
    operator: str
    owner: str
    token_id: str


class Operator(BaseModel):
    key: Key1
    value: Dict[str, Any]


class TokenMetadata(BaseModel):
    token_id: str
    token_info: Dict[str, str]


class Storage(BaseModel):
    administrator: str
    all_tokens: str
    ledger: Union[int, List[LedgerItem]]
    metadata: Union[int, Dict[str, str]]
    operators: Union[int, List[Operator]]
    paused: bool
    token_metadata: Union[int, Dict[str, TokenMetadata]]
