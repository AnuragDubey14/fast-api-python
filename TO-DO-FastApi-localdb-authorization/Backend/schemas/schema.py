from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Pydantic model for Task (used for request data)
class TaskSchema(BaseModel):
    task_id: Optional[int] = None
    title: str
    description: str
    status: bool
    created_at: datetime
    updated_at: datetime
    deadline: datetime

    model_config = {
        "from_attributes": True  # This allows Pydantic to work with ORM objects
    }

class UserCreate(BaseModel):
    user_id: Optional[int] = None
    user_name: str
    user_password: str

class UserSchema(BaseModel):
    user_id: int
    user_name: str
    user_password: str

    model_config = {
        "from_attributes": True
    }

# Pydantic model for TaskResponse (used for response data)
class TaskResponse(BaseModel):
    task_id: int 
    title: str
    description: str
    status: bool
    created_at: datetime  
    updated_at: datetime  
    deadline: datetime
    owner_id: int 

    model_config = {
        "from_attributes": True
    }

class TaskStatusUpdate(BaseModel):
    status: bool

class TaskDeadlineUpdate(BaseModel):
    deadline: datetime
