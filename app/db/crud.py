# 数据库操作函数 
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import history as schemas
from typing import Optional, List

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