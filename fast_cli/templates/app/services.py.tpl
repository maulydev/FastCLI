from sqlalchemy.orm import Session
from .models import Todo
from .schemas import TodoCreate, TodoUpdate

def get_all(db: Session):
    return db.query(Todo).all()

def create(db: Session, data: TodoCreate):
    todo = Todo(**data.dict())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def update(db: Session, todo_id: int, data: TodoUpdate):
    todo = db.query(Todo).get(todo_id)
    if todo:
        for key, value in data.dict().items():
            setattr(todo, key, value)
        db.commit()
        db.refresh(todo)
    return todo

def delete(db: Session, todo_id: int):
    todo = db.query(Todo).get(todo_id)
    if todo:
        db.delete(todo)
        db.commit()
    return todo
