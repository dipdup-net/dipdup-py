# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class Records(BaseModel):
    address: Optional[str]
    data: Dict[str, str]
    expiry_key: Optional[str]
    internal_data: Dict[str, str]
    level: str
    owner: str
    tzip12_token_id: Optional[str]


class ReverseRecords(BaseModel):
    internal_data: Dict[str, str]
    name: Optional[str]
    owner: str


class Store(BaseModel):
    data: Union[int, Dict[str, str]]
    expiry_map: Union[int, Dict[str, str]]
    metadata: Union[int, Dict[str, str]]
    next_tzip12_token_id: str
    owner: str
    records: Union[int, Dict[str, Records]]
    reverse_records: Union[int, Dict[str, ReverseRecords]]
    tzip12_tokens: Union[int, Dict[str, str]]


class Storage(BaseModel):
    actions: Union[int, Dict[str, str]]
    store: Store
    trusted_senders: List[str]
