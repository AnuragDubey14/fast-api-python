from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from config.db import get_db
from models.index import Task
from schemas.schema import Task as TaskSchema, TaskResponse

taskRouter = APIRouter()


# Get all tasks
@taskRouter.get('/get-tasks', response_model=list[TaskResponse])
async def all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return [TaskResponse.model_validate(task) for task in tasks]


# Get task by ID or Title
@taskRouter.get('/get-task/', response_model=TaskResponse)
async def get_task(id: int | None = None, title: str | None = None, db: Session = Depends(get_db)):
    if id:
        task = db.query(Task).filter(Task.id == id).first()
    elif title:
        task = db.query(Task).filter(Task.title == title).first()
    else:
        raise HTTPException(status_code=400, detail="Please provide either task ID or title")

    if task:
        return TaskResponse.model_validate(task)

    raise HTTPException(status_code=404, detail="Task not found")


# Add a new task
@taskRouter.post('/add-task')
async def add_task(task: TaskSchema, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return {"message": "Task added successfully", "task": new_task}
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Task with this title already exists")


# Update task by ID or Title
@taskRouter.put('/update-task/', response_model=TaskResponse)
async def update_task(
    id: int | None = None,
    title: str | None = None,
    task: TaskSchema = Body(...),
    db: Session = Depends(get_db)
):
    query = None

    if id:
        query = db.query(Task).filter(Task.id == id)
    elif title:
        query = db.query(Task).filter(Task.title == title)
    else:
        raise HTTPException(status_code=400, detail="Please provide either task ID or title")

    existing_task = query.first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.status = task.status

    db.commit()
    db.refresh(existing_task)
    return TaskResponse.model_validate(existing_task)


# Delete task by ID or Title
@taskRouter.delete('/delete-task/', response_model=dict)
async def delete_task(id: int | None = None, title: str | None = None, db: Session = Depends(get_db)):
    query = None

    if id:
        query = db.query(Task).filter(Task.id == id)
    elif title:
        query = db.query(Task).filter(Task.title == title)
    else:
        raise HTTPException(status_code=400, detail="Please provide either task ID or title")

    task = query.first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
