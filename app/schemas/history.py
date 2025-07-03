# 历史 Pydantic 模型 
from pydantic import BaseModel
from typing import Optional

class HistoryBase(BaseModel):
    country: str
    title: str
    content: str
    year: Optional[int] = None

class HistoryCreate(HistoryBase):
    pass

class History(HistoryBase):
    id: int

    class Config:
        orm_mode = True 