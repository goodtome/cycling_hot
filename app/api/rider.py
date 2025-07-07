from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import SessionLocal
from app.db import crud
from app.schemas import rider as schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Rider])
def read_riders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_riders(db, skip=skip, limit=limit)

@router.get("/{rider_id}", response_model=schemas.Rider)
def read_rider(rider_id: int, db: Session = Depends(get_db)):
    db_rider = crud.get_rider(db, rider_id)
    if db_rider is None:
        raise HTTPException(status_code=404, detail="车手未找到")
    return db_rider

@router.post("/", response_model=schemas.Rider)
def create_rider(rider: schemas.RiderCreate, db: Session = Depends(get_db)):
    return crud.create_rider(db, rider)

@router.put("/{rider_id}", response_model=schemas.Rider)
def update_rider(rider_id: int, rider: schemas.RiderCreate, db: Session = Depends(get_db)):
    db_rider = crud.update_rider(db, rider_id, rider)
    if db_rider is None:
        raise HTTPException(status_code=404, detail="车手未找到")
    return db_rider

@router.delete("/{rider_id}")
def delete_rider(rider_id: int, db: Session = Depends(get_db)):
    success = crud.delete_rider(db, rider_id)
    if not success:
        raise HTTPException(status_code=404, detail="车手未找到")
    return {"ok": True} 