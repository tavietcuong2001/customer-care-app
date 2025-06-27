from pydantic import BaseModel
from typing import List
from enum import IntEnum


class Message(BaseModel):
    role: str
    content: str


class Service(IntEnum):
    VI_DIEN_TU = 1
    CONG_THANH_TOAN = 2
    POS = 3
    CONG_1400 = 4


class Query(BaseModel):
    query: str
    chat_history: List[Message]
    service: Service
    chat_id: int


class Status(IntEnum):
    cont = 1
    done = 2
    forward = 3


class Response(BaseModel):
    answer: str
    status: Status
    chat_id: int