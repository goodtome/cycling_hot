# 数据库操作函数 
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import history as schemas
from typing import Optional, List
from app.schemas import team as team_schemas, rider as rider_schemas

# 创建历史条目
def create_history(db: Session, history: schemas.HistoryCreate):
    db_history = models.History(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

# 获取所有历史条目（按year升序）
def get_histories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.History).order_by(models.History.year.asc()).offset(skip).limit(limit).all()

# 按条件查询历史条目
def query_histories(db: Session, country: Optional[str] = None, year: Optional[int] = None, title: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[models.History]:
    query = db.query(models.History)
    if country:
        query = query.filter(models.History.country == country)
    if year:
        query = query.filter(models.History.year == year)
    if title:
        query = query.filter(models.History.title.like(f"%{title}%"))
    return query.order_by(models.History.year.asc()).offset(skip).limit(limit).all()

# 获取单条历史条目
def get_history(db: Session, history_id: int) -> Optional[models.History]:
    return db.query(models.History).filter(models.History.id == history_id).first()

# 删除历史条目
def delete_history(db: Session, history_id: int) -> bool:
    db_history = db.query(models.History).filter(models.History.id == history_id).first()
    if db_history:
        db.delete(db_history)
        db.commit()
        return True
    return False

# 修改历史条目
def update_history(db: Session, history_id: int, history: schemas.HistoryCreate):
    db_history = db.query(models.History).filter(models.History.id == history_id).first()
    if db_history:
        db_history.country = history.country
        db_history.title = history.title
        db_history.content = history.content
        db_history.year = history.year
        db.commit()
        db.refresh(db_history)
        return db_history
    return None 

# 车队相关操作

def create_team(db: Session, team: team_schemas.TeamCreate):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def update_team(db: Session, team_id: int, team: team_schemas.TeamCreate):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team:
        for field, value in team.dict().items():
            setattr(db_team, field, value)
        db.commit()
        db.refresh(db_team)
        return db_team
    return None

def delete_team(db: Session, team_id: int):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team:
        db.delete(db_team)
        db.commit()
        return True
    return False

# 车手相关操作

def create_rider(db: Session, rider: rider_schemas.RiderCreate):
    db_rider = models.Rider(**rider.dict())
    db.add(db_rider)
    db.commit()
    db.refresh(db_rider)
    return db_rider

def get_riders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rider).offset(skip).limit(limit).all()

def get_rider(db: Session, rider_id: int):
    return db.query(models.Rider).filter(models.Rider.id == rider_id).first()

def update_rider(db: Session, rider_id: int, rider: rider_schemas.RiderCreate):
    db_rider = db.query(models.Rider).filter(models.Rider.id == rider_id).first()
    if db_rider:
        for field, value in rider.dict().items():
            setattr(db_rider, field, value)
        db.commit()
        db.refresh(db_rider)
        return db_rider
    return None

def delete_rider(db: Session, rider_id: int):
    db_rider = db.query(models.Rider).filter(models.Rider.id == rider_id).first()
    if db_rider:
        db.delete(db_rider)
        db.commit()
        return True
    return False 