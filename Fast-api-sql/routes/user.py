from fastapi import APIRouter
from config.db import conn
from models.index import users
from schemas.index import User, UserResponse

user = APIRouter()

# Get all users
@user.get('/get-users', response_model=list[UserResponse])
async def all_user():
    users_data = conn.execute(users.select()).fetchall()
    return [UserResponse.model_validate(row) for row in users_data]

# Get user by ID
@user.get('/get-user/{id}', response_model=UserResponse)
async def get_user(id: int):
    user_data = conn.execute(users.select().where(users.c.id == id)).fetchall()
    if user_data is not None and user_data:
        return UserResponse.model_validate(user_data[0])
    return {"message": "User not found"}, 404

# Add a new user
@user.post('/add-user')
async def add_user(user: User):
    conn.execute(users.insert().values(
        name=user.name,
        email=user.email,
        password=user.password
    ))
    return {"message": "User added successfully", "user": user}

# Update user by ID
@user.put('/update-user/{id}', response_model=UserResponse)
async def update_user(id: int, user: User):
    conn.execute(users.update().where(users.c.id == id).values(
        name=user.name,
        email=user.email,
        password=user.password
    ))
    updated_user = conn.execute(users.select().where(users.c.id == id)).fetchall()
    return UserResponse.model_validate(updated_user[0])

# Delete user by ID
@user.delete('/delete-user/{id}')
async def delete_user(id: int):
    conn.execute(users.delete().where(users.c.id == id))
    return {"message": "User deleted successfully"}
