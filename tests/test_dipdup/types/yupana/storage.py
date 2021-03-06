# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Union

from pydantic import BaseModel
from pydantic import Extra


class Key(BaseModel):
    class Config:
        extra = Extra.forbid

    address: str
    nat: str


class LedgerItem(BaseModel):
    class Config:
        extra = Extra.forbid

    key: Key
    value: str


class Key1(BaseModel):
    class Config:
        extra = Extra.forbid

    address: str
    nat: str


class Value(BaseModel):
    class Config:
        extra = Extra.forbid

    allowances: List[str]
    borrow: str
    lastBorrowIndex: str


class Account(BaseModel):
    class Config:
        extra = Extra.forbid

    key: Key1
    value: Value


class MainTokenItem(BaseModel):
    class Config:
        extra = Extra.forbid

    fA12: str


class FA2(BaseModel):
    class Config:
        extra = Extra.forbid

    address: str
    nat: str


class MainTokenItem1(BaseModel):
    class Config:
        extra = Extra.forbid

    fA2: FA2


class Tokens(BaseModel):
    class Config:
        extra = Extra.forbid

    mainToken: Union[MainTokenItem, MainTokenItem1]
    interestRateModel: str
    interestUpdateTime: str
    priceUpdateTime: str
    totalBorrowsF: str
    totalLiquidF: str
    totalSupplyF: str
    totalReservesF: str
    borrowIndex: str
    maxBorrowRate: str
    collateralFactorF: str
    reserveFactorF: str
    lastPrice: str
    borrowPause: bool
    isInterestUpdating: bool
    threshold: str


class TokenMetadata(BaseModel):
    class Config:
        extra = Extra.forbid

    token_id: str
    tokens: Dict[str, str]


class KeyItem(BaseModel):
    class Config:
        extra = Extra.forbid

    fA12: str


class FA21(BaseModel):
    class Config:
        extra = Extra.forbid

    address: str
    nat: str


class KeyItem1(BaseModel):
    class Config:
        extra = Extra.forbid

    fA2: FA21


class Asset(BaseModel):
    class Config:
        extra = Extra.forbid

    key: Union[KeyItem, KeyItem1]
    value: str


class Storage(BaseModel):
    class Config:
        extra = Extra.forbid

    admin: str
    ledger: List[LedgerItem]
    accounts: List[Account]
    tokens: Dict[str, Tokens]
    metadata: Dict[str, str]
    tokenMetadata: Dict[str, TokenMetadata]
    lastTokenId: str
    priceFeedProxy: str
    closeFactorF: str
    liqIncentiveF: str
    markets: Dict[str, List[str]]
    borrows: Dict[str, List[str]]
    maxMarkets: str
    assets: List[Asset]


class YupanaStorage(BaseModel):
    class Config:
        extra = Extra.forbid

    storage: Storage
    tokenLambdas: Dict[str, str]
    useLambdas: Dict[str, str]
