from fastapi import APIRouter, HTTPException, Depends, Body,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Annotated
from dependencies import get_db,oauth2_scheme
from models.index import Task,User
from schemas.schema import TaskSchema, TaskResponse,UserSchema,UserCreate
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

taskRouter = APIRouter()


# JWT Configuration
SECRET_KEY = "your_secret_key"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

@taskRouter.post("/register", response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username already exists
    existing_user = db.query(User).filter(User.user_name == user.user_name).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Hash the password before saving
    hashed_password = pwd_context.hash(user.user_password)
    new_user = User(
        user_name=user.user_name,
        user_password=hashed_password
    )
    
    # Save the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@taskRouter.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Retrieve user by username from the database
    user = db.query(User).filter(User.user_name == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify the password using the hashing context
    if not pwd_context.verify(form_data.password, user.user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Define token expiration and generate JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# Get all tasks
@taskRouter.get('/tasks', response_model=list[TaskResponse])
async def all_tasks(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.owner_id==current_user.user_id).all()
    return [TaskResponse.model_validate(task) for task in tasks]


# Get task by ID or Title
@taskRouter.get('/task/', response_model=TaskResponse)
async def get_task(id: int | None = None, title: str | None = None, db: Session = Depends(get_db),token:str=Depends(oauth2_scheme),current_user: User = Depends(get_current_user)):
    if id:
        task = db.query(Task).filter(Task.task_id == id).first()
    elif title:
        task = db.query(Task).filter(Task.title == title).first()
    else:
        raise HTTPException(status_code=400, detail="Please provide either task ID or title")

    if task:
        if task.owner_id==current_user.user_id:
            return TaskResponse.model_validate(task)
        raise HTTPException(status_code=401,detail="You are unauthorized to see the details of this task")

    raise HTTPException(status_code=404, detail="Task not found")


# Add a new task
@taskRouter.post('/task/')
async def add_task(task: TaskSchema, db: Session = Depends(get_db),token:str=Depends(oauth2_scheme),current_user: User = Depends(get_current_user)):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        created_at=task.created_at,
        updated_at=task.updated_at,
        owner_id=current_user.user_id
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
@taskRouter.put('/task/', response_model=TaskResponse)
async def update_task(
    id: int | None = None,
    title: str | None = None,
    task: TaskSchema = Body(...),
    db: Session = Depends(get_db)
    ,token:str=Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user)
):
    query = None

    if id:
        query = db.query(Task).filter(Task.task_id == id)
    elif title:
        query = db.query(Task).filter(Task.title == title)
    else:
        raise HTTPException(status_code=400, detail="Please provide either task ID or title")

    existing_task = query.first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    elif existing_task.owner_id!=current_user.user_id:
        raise HTTPException(status_code=401,detail="You are unauthorized to update this task")

    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.status = task.status

    db.commit()
    db.refresh(existing_task)
    return TaskResponse.model_validate(existing_task)

@taskRouter.patch('/task',response_model=TaskResponse)
async def update_status(id:int|None,title:str|None, status:bool,task:TaskSchema=Body(...),db: Session=Depends(get_db),token:str=Depends(oauth2_scheme),current_user: User = Depends(get_current_user)):
    query = None

    if id:
        query = db.query(Task).filter(Task.task_id == id)
    elif title:
        query = db.query(Task).filter(Task.title == title)
    else:
        raise HTTPException(status_code=400, detail="Please provide either task ID or title")

    existing_task = query.first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    elif existing_task.owner_id!=current_user.user_id:
        raise HTTPException(status_code=401,detail="You are unauthorized to update status of this task")

    existing_task.status = task.status

    db.commit()
    db.refresh(existing_task)
    return TaskResponse.model_validate(existing_task)



# Delete task by ID or Title
@taskRouter.delete('/task/', response_model=dict)
async def delete_task(id: int | None = None, title: str | None = None, db: Session = Depends(get_db),token:str=Depends(oauth2_scheme),current_user: User = Depends(get_current_user)):
    query = None

    if id:
        query = db.query(Task).filter(Task.task_id == id)
    elif title:
        query = db.query(Task).filter(Task.title == title)
    else:
        raise HTTPException(status_code=400, detail="Please provide either task ID or title")

    task = query.first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.owner_id!=current_user.user_id:
        raise HTTPException(status_code=401,detail="You are unauthorized to delete this task")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
