from pydantic import BaseModel
from typing import Optional, List

class TeamBase(BaseModel):
    uci_code: str
    name: str
    country: str
    founded_year: int
    sponsor: Optional[str] = None
    former_names: Optional[List[str]] = None  # 历史名称
    note: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    class Config:
        orm_mode = True 