# generated by datamodel-codegen:
#   filename:  propose.json

from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel


class DiffItem(BaseModel):
    key: str
    new_value: Optional[str]


class ProposalType0(BaseModel):
    agora_post_id: str
    diff: List[DiffItem]


class ProposalMetadatum(BaseModel):
    proposal_type_0: ProposalType0


class ProposalType1(BaseModel):
    frozen_extra_value: Optional[str]
    frozen_scale_value: Optional[str]
    max_proposal_size: Optional[str]
    slash_division_value: Optional[str]
    slash_scale_value: Optional[str]


class ProposalMetadatum1(BaseModel):
    proposal_type_1: ProposalType1


class ProposalMetadatum2(BaseModel):
    receivers_0: List[str]


class ProposalMetadatum3(BaseModel):
    receivers_1: List[str]


class Propose(BaseModel):
    frozen_token: str
    proposal_metadata: Union[ProposalMetadatum, ProposalMetadatum1, ProposalMetadatum2, ProposalMetadatum3]
