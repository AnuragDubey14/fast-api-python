from pydantic import BaseModel
from datetime import datetime

# Pydantic model for Task (used for request data)
class TaskSchema(BaseModel):
    task_id: int
    title: str
    description: str
    status: bool
    created_at: datetime  # To capture the creation timestamp
    updated_at: datetime  # To capture the update timestamp

    class Config:
        from_attributes  = True  # This allows Pydantic to work with ORM objects


class UserCreate(BaseModel):
    user_id: int
    user_name: str
    user_password: str

class UserSchema(BaseModel):
    user_id: int
    user_name:str
    user_password:str

    class Config:
        from_attributes=True


# Pydantic model for TaskResponse (used for response data)
class TaskResponse(BaseModel):
    title: str
    description: str
    status: bool
    created_at: datetime  # To capture the creation timestamp
    updated_at: datetime  # To capture the update timestamp

    class Config:
        from_attributes  = True  # This allows Pydantic to work with ORM objects
