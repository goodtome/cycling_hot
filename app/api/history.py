from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.base import SessionLocal
from app.db import crud
from app.schemas import history as schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.History])
def read_histories(
    country: Optional[str] = Query(None, description="国家"),
    year: Optional[int] = Query(None, description="年份"),
    title: Optional[str] = Query(None, description="标题关键词"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if country or year or title:
        return crud.query_histories(db, country=country, year=year, title=title, skip=skip, limit=limit)
    return crud.get_histories(db, skip=skip, limit=limit)

@router.get("/{history_id}", response_model=schemas.History)
def read_history(history_id: int, db: Session = Depends(get_db)):
    db_history = crud.get_history(db, history_id)
    if db_history is None:
        raise HTTPException(status_code=404, detail="历史条目未找到")
    return db_history

@router.post("/", response_model=schemas.History)
def create_history(history: schemas.HistoryCreate, db: Session = Depends(get_db)):
    return crud.create_history(db, history)

@router.put("/{history_id}", response_model=schemas.History)
def update_history(history_id: int, history: schemas.HistoryCreate, db: Session = Depends(get_db)):
    db_history = crud.update_history(db, history_id, history)
    if db_history is None:
        raise HTTPException(status_code=404, detail="历史条目未找到")
    return db_history

@router.delete("/{history_id}")
def delete_history(history_id: int, db: Session = Depends(get_db)):
    success = crud.delete_history(db, history_id)
    if not success:
        raise HTTPException(status_code=404, detail="历史条目未找到")
    return {"ok": True} 