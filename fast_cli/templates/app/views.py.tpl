from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import TodoCreate, TodoUpdate, TodoOut
from .services import get_all, create, update, delete
from {{ project_name }}.database import SessionLocal
from fastapi import APIRouter

core_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@core_router.get("/", response_model=list[TodoOut])
def list_todos(db: Session = Depends(get_db)):
    return get_all(db)

@core_router.post("/", response_model=TodoOut)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return create(db, todo)

@core_router.put("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    updated = update(db, todo_id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated

@core_router.delete("/{todo_id}", response_model=TodoOut)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    deleted = delete(db, todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return deleted
