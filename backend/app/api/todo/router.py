from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.middleware.auth_middleware import get_current_user
from typing import List
import uuid

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_todo = Todo(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        title=todo.title,
        description=todo.description
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Todo).filter(Todo.user_id == current_user.id).all()

@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: str, todo: TodoUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}