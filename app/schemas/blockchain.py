from datetime import date

from pydantic import BaseModel


class DataCreate(BaseModel):
    data: dict

class SearchIndex(BaseModel):
    index: str

class SearchOut(BaseModel):
    data: dict

class DataOut(BaseModel):
    data: str

class BlockCreate(BaseModel):
    hash_value: str
    timestamp: str
    data: dict
    previous_hash: str
    index: int

class InfoOut(BaseModel):
    chain_length: int
    latest_block_hash: str
