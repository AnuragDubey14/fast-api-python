from pydantic import BaseModel
from datetime import datetime

# Pydantic model for Task (used for request data)
class Task(BaseModel):
    task_id: int
    title: str
    description: str
    status: bool
    created_at: datetime  # To capture the creation timestamp
    updated_at: datetime  # To capture the update timestamp

    class Config:
        from_attributes  = True  # This allows Pydantic to work with ORM objects

# Pydantic model for TaskResponse (used for response data)
class TaskResponse(BaseModel):
    title: str
    description: str
    status: bool
    created_at: datetime  # To capture the creation timestamp
    updated_at: datetime  # To capture the update timestamp

    class Config:
        from_attributes  = True  # This allows Pydantic to work with ORM objects
