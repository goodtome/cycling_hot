# 车手 Pydantic 模型 
from pydantic import BaseModel
from typing import Optional

class RiderBase(BaseModel):
    name_cn: str
    name_en: Optional[str] = None
    age: Optional[int] = None
    birth_date: Optional[str] = None
    current_team_id: Optional[int] = None
    former_teams: Optional[str] = None
    rider_type: Optional[str] = None
    achievements: Optional[str] = None
    note: Optional[str] = None
    nationality: Optional[str] = None
    gender: Optional[str] = None
    uci_id: Optional[str] = None

class RiderCreate(RiderBase):
    pass

class Rider(RiderBase):
    id: int
    class Config:
        orm_mode = True 