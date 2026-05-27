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
